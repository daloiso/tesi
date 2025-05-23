import { VStack, Text, Image, Divider } from "@chakra-ui/react";
import React, { useState, useEffect } from "react";

export default function ImageSlider({ title, text, index }) {
  const [imageSrc, setImageSrc] = useState("/img/150.png");
  useEffect(() => {
    
    fetchImageFromBackend();
  }, [index]);

  const fetchImageFromBackend = async () => {
    const imageUrl = await downloadImageUrl(title, index);
    setImageSrc(imageUrl);
  };
  
  return (
    <VStack>
      <Text fontSize="lg" >{text}</Text>
      <Image src={imageSrc} alt={text} />
      <Divider />
    </VStack>
  );
}

import axios from "axios";
const apiUrl = import.meta.env.VITE_API_URL;

async function downloadImageUrl(title, index) {
  const url =
    `${apiUrl}/api/files/?type=img&title=` +
    title +
    "&index=" +
    index;

  try {
    const response = await axios.get(url, {
      responseType: "blob",
      headers: {
        Authorization: "Token b9862aacb7a0c2f9b1a346e8e1186607e61ecf81",
      },
      withCredentials: true,
    });

    console.log("Data:", response.data);

    // Create a Blob from the response data
    const blob = new Blob([response.data], { type: "audio/mp3" });

    // Create a Blob URL to use in the AudioPlayer
    const blobUrl = URL.createObjectURL(blob);

    return blobUrl; // Return the Blob URL
  } catch (error) {
    console.error("Error:", error);
    return null;
  }
}
