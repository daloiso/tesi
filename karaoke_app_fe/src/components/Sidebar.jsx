import { List } from "@chakra-ui/react";
import { FaHome } from "react-icons/fa";
import { MdDashboard } from "react-icons/md";
import { GrContact } from "react-icons/gr";
import { NavLink } from "react-router-dom";
import { Link as ChakraLink, Stack } from "@chakra-ui/react";
const Sidebar = () => {
  return (
    <Stack>
      <ChakraLink asChild>
        <NavLink to="/">
          <FaHome />
          Home
        </NavLink>
      </ChakraLink>
      <ChakraLink asChild>
        <NavLink to="dashboard">
          <MdDashboard />
          Dashboard
        </NavLink>
      </ChakraLink>

      <ChakraLink asChild>
        <NavLink to="contact">
          <GrContact />
          Contact
        </NavLink>
      </ChakraLink>
    </Stack>
  );
};
export default Sidebar;
