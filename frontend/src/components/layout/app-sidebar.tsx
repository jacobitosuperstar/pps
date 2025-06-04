import {
  LayoutDashboard,
  Factory,
  Settings2,
  PackagePlus,
  Users,
} from "lucide-react";

import { NavMain } from "./nav-main";
import { NavSecondary } from "./nav-secondary";
import { NavUser } from "./nav-user";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { Link } from "react-router-dom";
import { PATHS } from "@/constant/paths";
import { useMemo } from "react";
import { useAppSelector } from "@/store/store";

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { user } = useAppSelector((store) => store.auth);

  const data = useMemo(() => {
    return {
      user: {
        name: user?.names || "",
        email: user?.identification || "",
        avatar: "/avatars/shadcn.jpg",
      },
      navMain: [
        {
          title: "Dashboard",
          url: "#",
          icon: LayoutDashboard,
        },
      ],
      configModules: [
        {
          title: "Maquinaria",
          url: "#",
          icon: Settings2,
        },
      ],
      masterModules: [
        {
          title: "Empleados",
          url: PATHS.EMPLOYEES,
          icon: Users,
        },
        {
          title: "Maquinaria",
          url: PATHS.MACHINES,
          icon: PackagePlus,
        },
      ],
    };
  }, [user]);

  return (
    <Sidebar collapsible="offcanvas" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              asChild
              className="data-[slot=sidebar-menu-button]:!p-1.5"
            >
              <Link to={PATHS.HOME}>
                <Factory className="h-5 w-5" />
                <span className="text-base font-semibold">PPS</span>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavSecondary title="Configuración" items={data.configModules} />
        <NavSecondary title="Maestros" items={data.masterModules} />
      </SidebarContent>
      <SidebarFooter>
        <NavUser user={data.user} />
      </SidebarFooter>
    </Sidebar>
  );
}
