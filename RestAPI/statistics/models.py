from typing import Optional, List, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# MACHINE STATISTICS
# ============================================================================

class MachineUtilization(BaseModel):
    """Machine utilization/occupancy metrics."""
    machine_id: int
    machine_code: str
    machine_name: str
    total_hours_in_period: float = Field(..., description="Total hours in the analysis period")
    production_hours: float = Field(..., description="Hours spent on production shifts")
    maintenance_hours: float = Field(..., description="Hours spent on maintenance")
    breakdown_hours: float = Field(..., description="Hours spent on machine breakdowns")
    setup_hours: float = Field(..., description="Hours spent on setup/changeover")
    idle_hours: float = Field(..., description="Hours machine was idle")
    utilization_percentage: float = Field(..., ge=0, le=100, description="Percentage of time machine was utilized")
    production_percentage: float = Field(..., ge=0, le=100, description="Percentage of time on production")

    model_config = ConfigDict(from_attributes=True)


class MachineUtilizationSummary(BaseModel):
    """Summary of all machines utilization."""
    period_start: datetime
    period_end: datetime
    total_machines: int
    average_utilization: float = Field(..., ge=0, le=100)
    machines: List[MachineUtilization]

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# QUALITY STATISTICS
# ============================================================================

class QualityMetrics(BaseModel):
    """Quality metrics for a specific period."""
    period_start: datetime
    period_end: datetime
    total_evaluations: int
    total_items_evaluated: int
    total_non_conforming_items: int
    defect_rate: float = Field(..., ge=0, le=100, description="Percentage of non-conforming items")
    quality_rate: float = Field(..., ge=0, le=100, description="Percentage of conforming items")
    evaluations_by_status: Dict[str, int] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class ProductQualityMetrics(BaseModel):
    """Quality metrics per product."""
    product_id: int
    product_name: str
    total_produced: int
    total_non_conforming: int
    defect_rate: float = Field(..., ge=0, le=100)
    quality_rate: float = Field(..., ge=0, le=100)

    model_config = ConfigDict(from_attributes=True)


class QualityIndicators(BaseModel):
    """Comprehensive quality indicators."""
    period_start: datetime
    period_end: datetime
    overall_metrics: QualityMetrics
    by_product: List[ProductQualityMetrics]

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# CLIENT STATISTICS
# ============================================================================

class ClientOrderMetrics(BaseModel):
    """Order metrics for a specific client."""
    client_id: str
    client_name: str
    total_orders: int
    total_items_ordered: int
    total_revenue: Optional[float] = Field(None, description="Total revenue from this client")
    most_ordered_product: Optional[str] = Field(None, description="Most frequently ordered product")
    most_ordered_product_quantity: Optional[int] = Field(None, description="Quantity of most ordered product")
    last_order_date: Optional[datetime] = Field(None, description="Date of last order")

    model_config = ConfigDict(from_attributes=True)


class ClientStatistics(BaseModel):
    """Statistics about clients."""
    period_start: datetime
    period_end: datetime
    total_clients: int
    total_orders: int
    average_orders_per_client: float
    top_clients: List[ClientOrderMetrics] = Field(..., description="Top clients by order volume")

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# EMPLOYEE PRODUCTIVITY STATISTICS
# ============================================================================

class EmployeeProductivity(BaseModel):
    """Productivity metrics for an employee."""
    employee_id: str
    employee_name: str
    employee_role: str
    total_shifts: int
    total_hours_worked: float
    production_shifts: int
    production_hours: float
    maintenance_shifts: int
    avg_shift_duration: float = Field(..., description="Average shift duration in hours")
    productivity_score: Optional[float] = Field(None, ge=0, le=100, description="Overall productivity score")

    model_config = ConfigDict(from_attributes=True)


class EmployeeProductivitySummary(BaseModel):
    """Summary of employee productivity."""
    period_start: datetime
    period_end: datetime
    total_employees: int
    total_shifts: int
    total_hours_worked: float
    average_hours_per_employee: float
    top_performers: List[EmployeeProductivity]

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# PRODUCTION EFFICIENCY STATISTICS
# ============================================================================

class ProductionEfficiency(BaseModel):
    """Production efficiency metrics."""
    period_start: datetime
    period_end: datetime
    total_production_orders: int
    completed_orders: int
    in_progress_orders: int
    cancelled_orders: int
    completion_rate: float = Field(..., ge=0, le=100, description="Percentage of completed orders")
    total_items_planned: int
    total_items_produced: int
    production_achievement: float = Field(..., ge=0, description="Percentage of planned production achieved")
    average_production_time: Optional[float] = Field(None, description="Average time to complete an order in hours")

    model_config = ConfigDict(from_attributes=True)


class ProductProductionMetrics(BaseModel):
    """Production metrics per product."""
    product_id: int
    product_name: str
    total_ordered: int
    total_produced: int
    production_efficiency: float = Field(..., ge=0, description="Ratio of produced to ordered")

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# SHIFT STATISTICS
# ============================================================================

class ShiftTypeDistribution(BaseModel):
    """Distribution of shifts by type."""
    shift_type: str
    count: int
    total_hours: float
    percentage: float = Field(..., ge=0, le=100)

    model_config = ConfigDict(from_attributes=True)


class ShiftStatistics(BaseModel):
    """Statistics about shifts."""
    period_start: datetime
    period_end: datetime
    total_shifts: int
    total_hours: float
    by_type: List[ShiftTypeDistribution]
    by_status: Dict[str, int]
    average_shift_duration: float

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# OOO (OUT OF OFFICE) IMPACT STATISTICS
# ============================================================================

class OOOImpactMetrics(BaseModel):
    """Metrics about OOO (Out of Office) impact."""
    period_start: datetime
    period_end: datetime
    total_ooo_records: int
    total_employees_affected: int
    total_days_lost: int
    ooo_by_type: Dict[str, int]
    impact_percentage: float = Field(..., ge=0, le=100, description="Percentage of potential work days lost to OOO")

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# COMPREHENSIVE DASHBOARD
# ============================================================================

class DashboardMetrics(BaseModel):
    """Comprehensive dashboard with all key metrics."""
    period_start: datetime
    period_end: datetime
    machine_utilization_avg: float = Field(..., ge=0, le=100)
    quality_rate: float = Field(..., ge=0, le=100)
    defect_rate: float = Field(..., ge=0, le=100)
    production_completion_rate: float = Field(..., ge=0, le=100)
    total_orders: int
    total_clients: int
    total_employees_active: int
    total_production_hours: float
    total_maintenance_hours: float
    ooo_impact_percentage: float = Field(..., ge=0, le=100)

    model_config = ConfigDict(from_attributes=True)
