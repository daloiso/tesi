import { FaRegPlayCircle } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";
import ReactGA from "react-ga4";

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
  useDisclosure
} from "@chakra-ui/react"
import { useLoaderData } from "react-router-dom"
import Player from "../components/Player"
import React, { useState } from 'react';

export default function Dashboard() {
  const tasks = useLoaderData()
  const [title, setTitle] = useState('Titolo iniziale');
  const { isOpen, onOpen, onClose } = useDisclosure();
  const playMusicFun = (title) => {
    onOpen();
    setTitle(title);
    if (process.env.NODE_ENV === "production") {
      ReactGA.event({
        category: 'Music',
        action: 'Play Song',
        label: title
      });
    }
  }
  console.log(process.env.NODE_ENV );
  if (process.env.NODE_ENV === "production") {
    ReactGA.send({ hitType: "pageview", page: "/dashboard", title: "dashboard" });
  }
  return (
    <div>
      <SimpleGrid spacing={10} minChildWidth={300}>
        {tasks && tasks.map(task => (
          <Card key={task.title} borderTop="8px" borderColor="purple.400" bg="white">

            <CardHeader color="gray.700">
              <Flex gap={5}>
                
                <Box>
                  <Heading as="h3" size="sm">{task.title}</Heading>
                
                </Box>
              </Flex>
            </CardHeader>

            <CardBody color="gray.500">
              <Text>{task.textSong}</Text>
            </CardBody>


            <CardFooter>
              <HStack>
                <Button variant="ghost" leftIcon={<FaRegPlayCircle />} onClick={() => playMusicFun(task.title)} >Play</Button>
              
                <Button variant="ghost" leftIcon={<IoMdDownload />}  onClick={() => donwloadMusicFun(task.title)} >Download</Button>
              </HStack>
            </CardFooter>

          </Card>
        ))}
      </SimpleGrid>
      <Player isOpen={isOpen} 
        onClose={onClose} 
        title={title} ></Player>
    </div>
  )
}


import axios from 'axios';
import { json } from 'react-router-dom';
const apiUrl = import.meta.env.VITE_API_URL;

export const tasksLoader = async () => {
  const url = `${apiUrl}/api/activity/`;

  return axios.get(url, {headers: {
      'Authorization': 'Token b9862aacb7a0c2f9b1a346e8e1186607e61ecf81',
      'Content-Type': 'application/json'
    },
    withCredentials: true,  
  })
    .then(response => {
      if(!localStorage.getItem('firstName')){
        response.data.pop();
      }
      console.log('Data:', response.data);
      return json(response.data);
    })
    .catch(error => {
      console.error('Error:', error);
      return json(null);
    });
}

async function donwloadMusicFun(title)  {
  const url = `${apiUrl}/api/files/?type=mp3&title=`+title;

  return axios.get(url, {
    responseType: "blob",
    headers: {
      'Authorization': 'Token b9862aacb7a0c2f9b1a346e8e1186607e61ecf81',
      
    },
    withCredentials: true,  
  })
    .then(response => {
      console.log('Data:', response.data);
      const blob = new Blob([response.data], { type: "audio/mp3" });

      // Create a link to trigger the download
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = title+".mp3"; // Set the name of the file
      link.setAttribute("download", title+".mp3");
      link.click();
      
    })
    .catch(error => {
      console.error('Error:', error);
      return null;
    });
  }

  