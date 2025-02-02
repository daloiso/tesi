import {
  Flex,
  Heading,
  Text,
  Button,
  Spacer,
  HStack,
  useToast,
} from "@chakra-ui/react";
import { GoogleOAuthProvider, GoogleLogin } from "@react-oauth/google";
import * as jwt_decode from "jwt-decode";
import React, { useState } from 'react';

import axios from "axios";
import { json } from "react-router-dom";
const apiUrl = import.meta.env.VITE_API_URL;

export const searchProfile = async (email) => {
  const url = `${apiUrl}/api/profile?search=${email}`;

  return axios
    .get(url, {
      headers: {
        "Content-Type": "application/json",
      },
      withCredentials: true,
    })
    .then((response) => {
      console.log("Data:", response.data);
      return json(response.data);
    })
    .catch((error) => {
      console.error("Error:", error);
      return json(null);
    });
};

export const getToken = async (email, password) => {
  const url = `${apiUrl}/api/login/`;

  return axios
    .post(
      url,
      {
        username: email,
        password: password,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    )
    .then((response) => {
      console.log("Data:", response.data);
      return json(response.data);
    })
    .catch((error) => {
      console.error("Error:", error);
      return json(null);
    });
};

export const saveProfile = async (email, firstName, lastName) => {
  const url = `${apiUrl}/api/profile/`;

  return axios
    .post(
      url,
      {
        email: email,
        name: firstName,
        password: lastName,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
        withCredentials: true,
      }
    )
    .then((response) => {
      console.log("Data:", response.data);
      return json(response.data);
    })
    .catch((error) => {
      console.error("Error:", error);
      return json(null);
    });
};

export default function Navbar() {
  const toast = useToast();
  const [nome, setNome] = useState(localStorage.getItem('firstName'));

  const handleLoginSuccess = async (response) => {
    console.log("Google Login Success:", response);
    // Qui puoi inviare il token a backend per autenticazione o usarlo direttamente
    const token = response.credential;
    const decodedToken = jwt_decode.jwtDecode(token);
    console.log(decodedToken);
    const name = decodedToken.name; // Nome completo
    const firstName = decodedToken.given_name; // Nome
    const lastName = decodedToken.family_name; // Cognome
    const email = decodedToken.email; // Email

    console.log(`Nome: ${firstName}`);
    console.log(`Cognome: ${lastName}`);
    console.log(`Email: ${email}`);
    //let profile = await searchProfile(email);
    //console.log(profile);
    //if (profile.length == 0) {
      let profileSaved = await saveProfile(email, firstName, lastName);
    //}
    let tokenProfile = await getToken(email,lastName);
    localStorage.setItem('authToken', tokenProfile.token);
    localStorage.setItem('firstName', firstName);
    localStorage.setItem('lastName', lastName);
    localStorage.setItem('email', email);
    //localStorage.getItem();
    setNome(firstName);
  };

  const handleLoginFailure = (error) => {
    console.error("Google Login Failed:", error);
    alert("login failure");
  };

  return (
    <Flex as="nav" p="10px" mb="60px" alignItems="center">
      <Heading as="h1" fontSize="1.5em">
        <Text
          fontSize="2xl"
          fontWeight="bold"
          color="teal.500"
          textAlign="center"
          mb={4}
        >
          Karaoke didattico
        </Text>
      </Heading>
      <Spacer />

      <HStack spacing="20px">
        <GoogleOAuthProvider clientId="173949360126-78n5ve6cd91s7k3bdpv6g0latcm6hkg9.apps.googleusercontent.com">
          <div>
            {!nome ? (
              <GoogleLogin
                onSuccess={handleLoginSuccess}
                onError={handleLoginFailure}
              />
            ) : (
              <Text fontSize="xl" fontWeight="bold" color="teal.500" mb={4}>
                Ciao {nome}
              </Text>
            )}
          </div>
        </GoogleOAuthProvider>
      </HStack>
    </Flex>
  );
}
