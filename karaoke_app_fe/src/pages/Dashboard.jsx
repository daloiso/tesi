import { FaRegPlayCircle } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";

import { 
  Box, 
  SimpleGrid,
  Text,
  Flex,
  Heading,
  Card, 
  CardHeader,
  CardBody,
  CardFooter,
  HStack,
  
  Button,
  Avatar
} from "@chakra-ui/react"
import { useLoaderData } from "react-router-dom"

export default function Dashboard() {
  const tasks = useLoaderData()

  return (
    <SimpleGrid spacing={10} minChildWidth={300}>
      {tasks && tasks.map(task => (
        <Card key={task.id} borderTop="8px" borderColor="purple.400" bg="white">

          <CardHeader color="gray.700">
            <Flex gap={5}>
              <Box w="50px" h="50px">
              <Avatar name={task.author} src={task.img} />
              </Box>
              <Box>
                <Heading as="h3" size="sm">{task.title}</Heading>
                <Text>by {task.author}</Text>
              </Box>
            </Flex>
          </CardHeader>

          <CardBody color="gray.500">
            <Text>{task.description}</Text>
          </CardBody>


          <CardFooter>
            <HStack>
              <Button variant="ghost" leftIcon={<FaRegPlayCircle />}>Play</Button>
              <Button variant="ghost" leftIcon={<IoMdDownload />}>Download</Button>
            </HStack>
          </CardFooter>

        </Card>
      ))}
    </SimpleGrid>
  )
}

export const tasksLoader = async () => {
  const res = await fetch('http://localhost:8000/activity')

  return res.json()
}