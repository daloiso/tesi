import { List, ListItem } from "@chakra-ui/react"
import { FaHome } from "react-icons/fa";
import { MdDashboard } from "react-icons/md";
import { GrContact } from "react-icons/gr";
import { NavLink } from "react-router-dom"


const Sidebar = () => {
  return (
    <List color="custom.text" fontSize="1.2em" spacing={4}>
      <ListItem>
        <NavLink to="/">
          <FaHome />
          Home
        </NavLink>
      </ListItem>
      <ListItem>
        <NavLink to="dashboard">
          <MdDashboard />
          Dashboard
        </NavLink>
      </ListItem>
      <ListItem>
        <NavLink to="contact">
          <GrContact />
          Contact
        </NavLink>
      </ListItem>
    </List>
  );
};
export default Sidebar;
