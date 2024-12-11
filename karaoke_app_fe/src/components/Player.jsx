import React, { useState, useEffect } from "react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  Text,
  ModalFooter,
  Button,
  ModalOverlay,
  Box
} from "@chakra-ui/react";
import AudioPlayer, { RHAP_UI } from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import ImageSlider from "./ImageSlider";

export default function Player({ isOpen, onClose, title }) {
  const [loading, setLoading] = useState(false);
  const [audioSrc, setAudioSrc] = useState(null);
  const [text, setText] = useState(null);
  const [index, setIndex] = useState(null);

  useEffect(() => {
    if (isOpen) {
      // Quando il modal si apre, effettua la chiamata al backend
      fetchDataFromBackend();
    }
  }, [isOpen]);

  const fetchDataFromBackend = async () => {
    setLoading(true); // Imposta lo stato di caricamento
    try {
      let data = await verseLoader(title);
      console.log(data);
      setText(data[0].wordsToDisplay);
      setIndex(0);
      const audioUrl = await downloadMusicUrl(title);
      setAudioSrc(audioUrl);
    } catch (error) {
      console.error("Errore durante la chiamata al backend:", error);
    } finally {
      setLoading(false); // Dopo aver ricevuto i dati, ferma il caricamento
    }
  };

  const OverlayOne = () => (
    <ModalOverlay
      bg="none"
      backdropFilter="auto"
      backdropInvert="80%"
      backdropBlur="2px"
    />
  );

  return (
    <Modal isCentered isOpen={isOpen} onClose={onClose}>
      {OverlayOne()}
      <ModalContent bg="yellowCustom">
        <ModalHeader>{title}</ModalHeader>
        <ModalBody>
          {loading ? (
            <Text color="gray.500">Caricamento dei dati in corso...</Text> // Messaggio di caricamento
          ) : (
            <Box>
              <ImageSlider
                index={index}
                title={title}
                text={text}
              ></ImageSlider>
              <AudioPlayer
                autoPlay
                src={audioSrc}
                onPlay={(e) => console.log("onPlay")}
                showJumpControls={false}
                showDownloadProgress={false}
                showFilledProgress={false}
                customControlsSection={[
                  RHAP_UI.MAIN_CONTROLS,
                  RHAP_UI.VOLUME_CONTROLS,
                ]}
              />
            </Box>
          )}
        </ModalBody>
        <ModalFooter>
          <Button bg="buttonCustom" color="white" onClick={onClose}>
            Close
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}

import axios from "axios";

async function downloadMusicUrl(title) {
  const url = "http://127.0.0.1:8000/api/files/?type=mp3&title=" + title;

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

async function downloadWorldUrl(title, sentence) {
  const url =
    "http://127.0.0.1:8000/api/files/?type=sentence&title=" +
    title +
    "&sentencePar=" +
    sentence;

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

export const verseLoader = async (title) => {
  const url = "http://127.0.0.1:8000/api/verse/?title=" + title;

  return axios
    .get(url, {
      headers: {
        Authorization: "Token b9862aacb7a0c2f9b1a346e8e1186607e61ecf81",
        "Content-Type": "application/json",
      },
      withCredentials: true,
    })
    .then((response) => {
      console.log("Data:", response.data);
      return response.data;
    })
    .catch((error) => {
      console.error("Error:", error);
      return null;
    });
};
