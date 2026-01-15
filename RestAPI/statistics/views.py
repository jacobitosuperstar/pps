from typing import Optional, List, Dict
from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from database import get_session
from jwt_authentication.decorators import get_current_user
from employees.models import RoleChoices, DBEmployee, DBOOO
from employees.utils import require_roles

from .models import (
    MachineUtilization,
    MachineUtilizationSummary,
    QualityMetrics,
    QualityIndicators,
    ProductQualityMetrics,
    ClientOrderMetrics,
    ClientStatistics,
    EmployeeProductivity,
    EmployeeProductivitySummary,
    ProductionEfficiency,
    ProductProductionMetrics,
    ShiftTypeDistribution,
    ShiftStatistics,
    OOOImpactMetrics,
    DashboardMetrics,
)

from machines.models import DBMachine
from shift.models import DBShift, ShiftType, ShiftStatus
from production.models import (
    DBSaleOrder,
    DBSaleOrderItem,
    DBProductionOrder,
    ProductionOrderStatus,
    DBQualityEvaluation,
    DBNonConformingProduct,
)
from clients.models import DBClient
from products.models import DBProduct


router: APIRouter = APIRouter(
    prefix="/statistics",
    tags=["statistics"],
)


def parse_datetime_param(dt_str: Optional[str]) -> Optional[datetime]:
    """Parse datetime string parameter."""
    if not dt_str:
        return None
    try:
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid datetime format: {dt_str}. Use ISO format."
        )


# ============================================================================
# MACHINE UTILIZATION ENDPOINTS
# ============================================================================

@router.get("/machine-utilization", response_model=MachineUtilizationSummary)
def get_machine_utilization(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    machine_id: Optional[int] = Query(None, description="Filter by specific machine"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> MachineUtilizationSummary:
    """
    Get machine utilization metrics for a given period.
    Shows how much time each machine spent on production, maintenance, breakdowns, etc.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT, RoleChoices.PRODUCTION_MANAGER]
    )

    # Default to last 30 days if not specified
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Calculate total hours in period
    total_hours_in_period = (period_end - period_start).total_seconds() / 3600

    # Get all machines or specific machine
    machines_query = session.query(DBMachine).filter(DBMachine.deleted == False)
    if machine_id:
        machines_query = machines_query.filter(DBMachine.id == machine_id)

    machines = machines_query.all()

    machine_utilizations = []

    for machine in machines:
        # Get all shifts for this machine in the period
        shifts = session.query(DBShift).filter(
            DBShift.machine_id == machine.id,
            DBShift.deleted == False,
            DBShift.start_datetime >= period_start,
            DBShift.end_datetime <= period_end
        ).all()

        # Calculate hours by shift type
        production_hours = 0
        maintenance_hours = 0
        breakdown_hours = 0
        setup_hours = 0
        other_hours = 0

        for shift in shifts:
            duration = (shift.end_datetime - shift.start_datetime).total_seconds() / 3600

            if shift.shift_type == ShiftType.PRODUCTION.value:
                production_hours += duration
            elif shift.shift_type == ShiftType.MAINTENANCE.value:
                maintenance_hours += duration
            elif shift.shift_type == ShiftType.MACHINE_BROKEN.value:
                breakdown_hours += duration
            elif shift.shift_type == ShiftType.SETUP.value:
                setup_hours += duration
            else:
                other_hours += duration

        total_working_hours = production_hours + maintenance_hours + breakdown_hours + setup_hours + other_hours
        idle_hours = max(0, total_hours_in_period - total_working_hours)

        utilization_percentage = (total_working_hours / total_hours_in_period * 100) if total_hours_in_period > 0 else 0
        production_percentage = (production_hours / total_hours_in_period * 100) if total_hours_in_period > 0 else 0

        machine_utilizations.append(MachineUtilization(
            machine_id=machine.id,
            machine_code=machine.machine_code,
            machine_name=machine.name,
            total_hours_in_period=total_hours_in_period,
            production_hours=production_hours,
            maintenance_hours=maintenance_hours,
            breakdown_hours=breakdown_hours,
            setup_hours=setup_hours,
            idle_hours=idle_hours,
            utilization_percentage=round(utilization_percentage, 2),
            production_percentage=round(production_percentage, 2),
        ))

    # Calculate average utilization
    avg_utilization = sum(m.utilization_percentage for m in machine_utilizations) / len(machine_utilizations) if machine_utilizations else 0

    return MachineUtilizationSummary(
        period_start=period_start,
        period_end=period_end,
        total_machines=len(machines),
        average_utilization=round(avg_utilization, 2),
        machines=machine_utilizations,
    )


# ============================================================================
# QUALITY INDICATORS ENDPOINTS
# ============================================================================

@router.get("/quality-indicators", response_model=QualityIndicators)
def get_quality_indicators(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> QualityIndicators:
    """
    Get quality indicators including defect rates and quality metrics.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT, RoleChoices.QUALITY, RoleChoices.PRODUCTION_MANAGER]
    )

    # Default to last 30 days
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Get quality evaluations in period
    evaluations = session.query(DBQualityEvaluation).filter(
        DBQualityEvaluation.deleted == False,
        DBQualityEvaluation.created_at >= period_start,
        DBQualityEvaluation.created_at <= period_end
    ).all()

    total_evaluations = len(evaluations)

    # Get all sale order items from these evaluations
    sale_order_ids = [e.sale_order_id for e in evaluations]
    total_items = session.query(func.count(DBSaleOrderItem.id)).filter(
        DBSaleOrderItem.sale_order_id.in_(sale_order_ids) if sale_order_ids else False
    ).scalar() or 0

    # Get non-conforming products
    evaluation_ids = [e.id for e in evaluations]
    total_non_conforming = session.query(func.count(DBNonConformingProduct.id)).filter(
        DBNonConformingProduct.quality_evaluation_id.in_(evaluation_ids) if evaluation_ids else False,
        DBNonConformingProduct.deleted == False
    ).scalar() or 0

    defect_rate = (total_non_conforming / total_items * 100) if total_items > 0 else 0
    quality_rate = 100 - defect_rate

    # Count evaluations by status (you can add status field to QualityEvaluation if needed)
    evaluations_by_status = {}

    overall_metrics = QualityMetrics(
        period_start=period_start,
        period_end=period_end,
        total_evaluations=total_evaluations,
        total_items_evaluated=total_items,
        total_non_conforming_items=total_non_conforming,
        defect_rate=round(defect_rate, 2),
        quality_rate=round(quality_rate, 2),
        evaluations_by_status=evaluations_by_status,
    )

    # Quality metrics by product
    product_metrics = []

    # Get all products that were evaluated
    products_in_evaluations = session.query(DBProduct).join(
        DBSaleOrderItem, DBProduct.id == DBSaleOrderItem.product_id
    ).filter(
        DBSaleOrderItem.sale_order_id.in_(sale_order_ids) if sale_order_ids else False
    ).distinct().all()

    for product in products_in_evaluations:
        # Count total items for this product
        product_items = session.query(func.sum(DBSaleOrderItem.product_amount)).filter(
            DBSaleOrderItem.product_id == product.id,
            DBSaleOrderItem.sale_order_id.in_(sale_order_ids) if sale_order_ids else False
        ).scalar() or 0

        # Count non-conforming for this product
        product_non_conforming = session.query(func.count(DBNonConformingProduct.id)).join(
            DBSaleOrderItem, DBNonConformingProduct.non_conforming_product_id == DBSaleOrderItem.id
        ).filter(
            DBSaleOrderItem.product_id == product.id,
            DBNonConformingProduct.quality_evaluation_id.in_(evaluation_ids) if evaluation_ids else False,
            DBNonConformingProduct.deleted == False
        ).scalar() or 0

        product_defect_rate = (product_non_conforming / product_items * 100) if product_items > 0 else 0

        product_metrics.append(ProductQualityMetrics(
            product_id=product.id,
            product_name=product.name,
            total_produced=int(product_items),
            total_non_conforming=product_non_conforming,
            defect_rate=round(product_defect_rate, 2),
            quality_rate=round(100 - product_defect_rate, 2),
        ))

    return QualityIndicators(
        period_start=period_start,
        period_end=period_end,
        overall_metrics=overall_metrics,
        by_product=product_metrics,
    )


# ============================================================================
# CLIENT STATISTICS ENDPOINTS
# ============================================================================

@router.get("/client-statistics", response_model=ClientStatistics)
def get_client_statistics(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    limit: int = Query(10, ge=1, le=100, description="Number of top clients to return"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ClientStatistics:
    """
    Get client statistics including top clients by order volume.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT, RoleChoices.ACCOUNTING]
    )

    # Default to last 30 days
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Get all clients with orders in period
    orders_in_period = session.query(DBSaleOrder).filter(
        DBSaleOrder.deleted == False,
        DBSaleOrder.created_at >= period_start,
        DBSaleOrder.created_at <= period_end
    ).all()

    total_orders = len(orders_in_period)

    # Group by client
    client_order_counts: Dict[str, Dict] = {}

    for order in orders_in_period:
        if order.client_id not in client_order_counts:
            client_order_counts[order.client_id] = {
                'total_orders': 0,
                'total_items': 0,
                'last_order_date': order.created_at,
                'products': {}
            }

        client_order_counts[order.client_id]['total_orders'] += 1
        client_order_counts[order.client_id]['last_order_date'] = max(
            client_order_counts[order.client_id]['last_order_date'],
            order.created_at
        )

        # Count items
        for item in order.items:
            client_order_counts[order.client_id]['total_items'] += item.product_amount

            # Track products ordered
            product_name = item.product.name if item.product else "Unknown"
            if product_name not in client_order_counts[order.client_id]['products']:
                client_order_counts[order.client_id]['products'][product_name] = 0
            client_order_counts[order.client_id]['products'][product_name] += item.product_amount

    # Build top clients list
    top_clients = []
    for client_id, data in client_order_counts.items():
        client = session.query(DBClient).filter_by(client_id=client_id).first()
        if not client:
            continue

        # Find most ordered product
        most_ordered_product = None
        most_ordered_quantity = 0
        if data['products']:
            most_ordered_product = max(data['products'], key=data['products'].get)
            most_ordered_quantity = data['products'][most_ordered_product]

        top_clients.append(ClientOrderMetrics(
            client_id=client_id,
            client_name=client.client_name,
            total_orders=data['total_orders'],
            total_items_ordered=data['total_items'],
            most_ordered_product=most_ordered_product,
            most_ordered_product_quantity=most_ordered_quantity,
            last_order_date=data['last_order_date'],
        ))

    # Sort by total orders descending and take top N
    top_clients.sort(key=lambda x: x.total_orders, reverse=True)
    top_clients = top_clients[:limit]

    total_clients = len(client_order_counts)
    avg_orders_per_client = total_orders / total_clients if total_clients > 0 else 0

    return ClientStatistics(
        period_start=period_start,
        period_end=period_end,
        total_clients=total_clients,
        total_orders=total_orders,
        average_orders_per_client=round(avg_orders_per_client, 2),
        top_clients=top_clients,
    )


# ============================================================================
# EMPLOYEE PRODUCTIVITY ENDPOINTS
# ============================================================================

@router.get("/employee-productivity", response_model=EmployeeProductivitySummary)
def get_employee_productivity(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    limit: int = Query(10, ge=1, le=100, description="Number of top performers to return"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> EmployeeProductivitySummary:
    """
    Get employee productivity metrics.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT, RoleChoices.HR, RoleChoices.PRODUCTION_MANAGER]
    )

    # Default to last 30 days
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Get all employees with shifts in period
    shifts_in_period = session.query(DBShift).filter(
        DBShift.deleted == False,
        DBShift.start_datetime >= period_start,
        DBShift.end_datetime <= period_end
    ).all()

    # Group by employee
    employee_metrics: Dict[str, Dict] = {}

    for shift in shifts_in_period:
        if shift.employee_id not in employee_metrics:
            employee_metrics[shift.employee_id] = {
                'total_shifts': 0,
                'total_hours': 0,
                'production_shifts': 0,
                'production_hours': 0,
                'maintenance_shifts': 0,
            }

        duration = (shift.end_datetime - shift.start_datetime).total_seconds() / 3600

        employee_metrics[shift.employee_id]['total_shifts'] += 1
        employee_metrics[shift.employee_id]['total_hours'] += duration

        if shift.shift_type == ShiftType.PRODUCTION.value:
            employee_metrics[shift.employee_id]['production_shifts'] += 1
            employee_metrics[shift.employee_id]['production_hours'] += duration
        elif shift.shift_type == ShiftType.MAINTENANCE.value:
            employee_metrics[shift.employee_id]['maintenance_shifts'] += 1

    # Build productivity list
    productivity_list = []
    total_hours_worked = 0

    for emp_id, data in employee_metrics.items():
        employee = session.query(DBEmployee).filter_by(identification=emp_id).first()
        if not employee:
            continue

        avg_shift_duration = data['total_hours'] / data['total_shifts'] if data['total_shifts'] > 0 else 0
        total_hours_worked += data['total_hours']

        productivity_list.append(EmployeeProductivity(
            employee_id=emp_id,
            employee_name=f"{employee.names} {employee.last_names}",
            employee_role=employee.role,
            total_shifts=data['total_shifts'],
            total_hours_worked=round(data['total_hours'], 2),
            production_shifts=data['production_shifts'],
            production_hours=round(data['production_hours'], 2),
            maintenance_shifts=data['maintenance_shifts'],
            avg_shift_duration=round(avg_shift_duration, 2),
        ))

    # Sort by total hours worked descending and take top N
    productivity_list.sort(key=lambda x: x.total_hours_worked, reverse=True)
    top_performers = productivity_list[:limit]

    total_employees = len(employee_metrics)
    avg_hours_per_employee = total_hours_worked / total_employees if total_employees > 0 else 0

    return EmployeeProductivitySummary(
        period_start=period_start,
        period_end=period_end,
        total_employees=total_employees,
        total_shifts=sum(data['total_shifts'] for data in employee_metrics.values()),
        total_hours_worked=round(total_hours_worked, 2),
        average_hours_per_employee=round(avg_hours_per_employee, 2),
        top_performers=top_performers,
    )


# ============================================================================
# PRODUCTION EFFICIENCY ENDPOINTS
# ============================================================================

@router.get("/production-efficiency", response_model=ProductionEfficiency)
def get_production_efficiency(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ProductionEfficiency:
    """
    Get production efficiency metrics.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT, RoleChoices.PRODUCTION_MANAGER]
    )

    # Default to last 30 days
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Get production orders in period
    production_orders = session.query(DBProductionOrder).filter(
        DBProductionOrder.deleted == False,
        DBProductionOrder.created_at >= period_start,
        DBProductionOrder.created_at <= period_end
    ).all()

    total_orders = len(production_orders)

    # Count by status using the new status field
    completed_orders = sum(1 for po in production_orders if po.status == ProductionOrderStatus.COMPLETED.value)
    in_progress_orders = sum(1 for po in production_orders if po.status == ProductionOrderStatus.IN_PROGRESS.value)
    cancelled_orders = sum(1 for po in production_orders if po.status == ProductionOrderStatus.CANCELLED.value)
    queued_orders = sum(1 for po in production_orders if po.status == ProductionOrderStatus.QUEUED.value)
    on_hold_orders = sum(1 for po in production_orders if po.status == ProductionOrderStatus.ON_HOLD.value)

    # Calculate total items planned from production order items
    total_items_planned = 0
    for po in production_orders:
        for item in po.items:
            total_items_planned += item.product_amount

    # For produced items, we count items from completed orders
    total_items_produced = 0
    for po in production_orders:
        if po.status == ProductionOrderStatus.COMPLETED.value:
            for item in po.items:
                total_items_produced += item.product_amount

    completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
    production_achievement = (total_items_produced / total_items_planned * 100) if total_items_planned > 0 else 0

    return ProductionEfficiency(
        period_start=period_start,
        period_end=period_end,
        total_production_orders=total_orders,
        completed_orders=completed_orders,
        in_progress_orders=in_progress_orders,
        cancelled_orders=cancelled_orders,
        completion_rate=round(completion_rate, 2),
        total_items_planned=total_items_planned,
        total_items_produced=total_items_produced,
        production_achievement=round(production_achievement, 2),
    )


# ============================================================================
# SHIFT STATISTICS ENDPOINTS
# ============================================================================

@router.get("/shift-statistics", response_model=ShiftStatistics)
def get_shift_statistics(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> ShiftStatistics:
    """
    Get shift statistics including distribution by type and status.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT, RoleChoices.PRODUCTION_MANAGER, RoleChoices.HR]
    )

    # Default to last 30 days
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Get all shifts in period
    shifts = session.query(DBShift).filter(
        DBShift.deleted == False,
        DBShift.start_datetime >= period_start,
        DBShift.end_datetime <= period_end
    ).all()

    total_shifts = len(shifts)
    total_hours = 0

    # Count by type
    type_counts: Dict[str, Dict] = {}
    status_counts: Dict[str, int] = {}

    for shift in shifts:
        duration = (shift.end_datetime - shift.start_datetime).total_seconds() / 3600
        total_hours += duration

        # By type
        if shift.shift_type not in type_counts:
            type_counts[shift.shift_type] = {'count': 0, 'hours': 0}
        type_counts[shift.shift_type]['count'] += 1
        type_counts[shift.shift_type]['hours'] += duration

        # By status
        status_counts[shift.status] = status_counts.get(shift.status, 0) + 1

    # Build type distribution
    by_type = []
    for shift_type, data in type_counts.items():
        percentage = (data['count'] / total_shifts * 100) if total_shifts > 0 else 0
        by_type.append(ShiftTypeDistribution(
            shift_type=shift_type,
            count=data['count'],
            total_hours=round(data['hours'], 2),
            percentage=round(percentage, 2),
        ))

    avg_shift_duration = total_hours / total_shifts if total_shifts > 0 else 0

    return ShiftStatistics(
        period_start=period_start,
        period_end=period_end,
        total_shifts=total_shifts,
        total_hours=round(total_hours, 2),
        by_type=by_type,
        by_status=status_counts,
        average_shift_duration=round(avg_shift_duration, 2),
    )


# ============================================================================
# OOO IMPACT ENDPOINTS
# ============================================================================

@router.get("/ooo-impact", response_model=OOOImpactMetrics)
def get_ooo_impact(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> OOOImpactMetrics:
    """
    Get Out of Office (OOO) impact metrics.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT, RoleChoices.HR]
    )

    # Default to last 30 days
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Get OOO records in period
    ooo_records = session.query(DBOOO).filter(
        DBOOO.deleted == False,
        DBOOO.start_date <= period_end,
        DBOOO.end_date >= period_start
    ).all()

    total_ooo = len(ooo_records)
    employees_affected = set()
    total_days_lost = 0
    ooo_by_type: Dict[str, int] = {}

    for ooo in ooo_records:
        employees_affected.add(ooo.employee_id)

        # Calculate overlap with period
        overlap_start = max(ooo.start_date, period_start)
        overlap_end = min(ooo.end_date, period_end)
        days = (overlap_end - overlap_start).days + 1
        total_days_lost += days

        # Count by type
        ooo_by_type[ooo.ooo_type] = ooo_by_type.get(ooo.ooo_type, 0) + 1

    # Calculate impact percentage
    # Assuming 8-hour workdays
    total_employee_count = session.query(func.count(DBEmployee.identification)).filter(
        DBEmployee.deleted == False
    ).scalar() or 1

    period_days = (period_end - period_start).days + 1
    total_potential_work_days = total_employee_count * period_days
    impact_percentage = (total_days_lost / total_potential_work_days * 100) if total_potential_work_days > 0 else 0

    return OOOImpactMetrics(
        period_start=period_start,
        period_end=period_end,
        total_ooo_records=total_ooo,
        total_employees_affected=len(employees_affected),
        total_days_lost=total_days_lost,
        ooo_by_type=ooo_by_type,
        impact_percentage=round(impact_percentage, 2),
    )


# ============================================================================
# DASHBOARD ENDPOINT
# ============================================================================

@router.get("/dashboard", response_model=DashboardMetrics)
def get_dashboard_metrics(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    token=Depends(get_current_user),
    session: Session = Depends(get_session),
) -> DashboardMetrics:
    """
    Get comprehensive dashboard with all key performance indicators.
    """
    require_roles(
        token,
        [RoleChoices.MANAGEMENT]
    )

    # Default to last 30 days
    period_end = parse_datetime_param(end_date) or datetime.now(UTC)
    period_start = parse_datetime_param(start_date) or (period_end - timedelta(days=30))

    # Get machine utilization average
    machine_util = get_machine_utilization(
        start_date=start_date,
        end_date=end_date,
        machine_id=None,
        token=token,
        session=session
    )

    # Get quality indicators
    quality = get_quality_indicators(
        start_date=start_date,
        end_date=end_date,
        token=token,
        session=session
    )

    # Get production efficiency
    production_eff = get_production_efficiency(
        start_date=start_date,
        end_date=end_date,
        token=token,
        session=session
    )

    # Get client statistics
    clients = get_client_statistics(
        start_date=start_date,
        end_date=end_date,
        limit=10,
        token=token,
        session=session
    )

    # Get shift statistics
    shifts = get_shift_statistics(
        start_date=start_date,
        end_date=end_date,
        token=token,
        session=session
    )

    # Get OOO impact
    ooo = get_ooo_impact(
        start_date=start_date,
        end_date=end_date,
        token=token,
        session=session
    )

    # Count active employees
    active_employees = session.query(func.count(DBEmployee.identification)).filter(
        DBEmployee.deleted == False
    ).scalar() or 0

    # Calculate production and maintenance hours
    production_hours = sum(
        t.total_hours for t in shifts.by_type
        if t.shift_type == ShiftType.PRODUCTION.value
    )
    maintenance_hours = sum(
        t.total_hours for t in shifts.by_type
        if t.shift_type == ShiftType.MAINTENANCE.value
    )

    return DashboardMetrics(
        period_start=period_start,
        period_end=period_end,
        machine_utilization_avg=machine_util.average_utilization,
        quality_rate=quality.overall_metrics.quality_rate,
        defect_rate=quality.overall_metrics.defect_rate,
        production_completion_rate=production_eff.completion_rate,
        total_orders=clients.total_orders,
        total_clients=clients.total_clients,
        total_employees_active=active_employees,
        total_production_hours=production_hours,
        total_maintenance_hours=maintenance_hours,
        ooo_impact_percentage=ooo.impact_percentage,
    )
