import { HStack, List, ListItem, Text } from "@chakra-ui/react"
import { FaHome } from "react-icons/fa";
import { MdDashboard } from "react-icons/md";
import { GrContact } from "react-icons/gr";
import { NavLink } from "react-router-dom"


const Sidebar = () => {
  return (
    <List color="custom.text" fontSize="1.2em" spacing={4}>
      <ListItem>
        <NavLink to="/">
          <HStack><FaHome /><Text>Home</Text></HStack>
        </NavLink>
      </ListItem>
      <ListItem>
        <NavLink to="dashboard">
        <HStack><MdDashboard /><Text>
          Dashboard</Text></HStack>
        </NavLink>
      </ListItem>
      <ListItem>
        <NavLink to="contact">
        <HStack><GrContact /><Text>
        
          Contact</Text></HStack>
        </NavLink>
      </ListItem>
    </List>
  );
};
export default Sidebar;
