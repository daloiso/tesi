import React, { useState, useEffect, useRef } from "react";
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
  Box,
  HStack
} from "@chakra-ui/react";
import AudioPlayer, { RHAP_UI } from "react-h5-audio-player";
import "react-h5-audio-player/lib/styles.css";
import ImageSlider from "./ImageSlider";
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import { Spinner } from '@chakra-ui/react'
import { FcOk } from "react-icons/fc";
import Fuse from "fuse.js";
import { ReactMediaRecorder } from 'react-media-recorder';

export default function Player({ isOpen, onClose, title, record }) {
  const [loading, setLoading] = useState(false);
  const [audioSrc, setAudioSrc] = useState(null);
  const [text, setText] = useState(null);
  const [index, setIndex] = useState(0);
  const [isListening, setIsListening] = useState(false);
  const [isRecording, setRecording] = useState(false);
  const [isBack, setBack] = useState(false);
  const [indexBack, setIndexBack] = useState(0);
  const indexBackRef = useRef(indexBack); // Use a ref to track the latest indexBack value
  const [isOK, setIsOK] = useState(false);
  const startRecordingBtnRef = useRef(null);
  const stopRecordingBtnRef = useRef(null);
  const { transcript, resetTranscript, listening } = useSpeechRecognition({
   
  });

  useEffect(() => {
    indexBackRef.current = indexBack;
  }, [indexBack]);

  useEffect(() => {
    if (isOpen) {
      // Quando il modal si apre, effettua la chiamata al backend
      fetchDataFromBackend();
    }
  }, [isOpen]);

  useEffect(() => {
    if (!isOpen) {
      if(record){
        if (stopRecordingBtnRef.current) {
          stopRecordingBtnRef.current.click()
        }
      }
      setIndexBack(0);
      onClose();
    }else{
      if(record){
        setRecording(true);
      }else{
        setRecording(false);
      }
    }
  }, [isOpen, onClose]);
  
  useEffect(() => {
    if (transcript) {
      console.log("Transcript updated:", transcript);
      const data = [{ text: text }];  // Wrap your `text` in an object

      // Fuse.js options with includeScore enabled
      const options = {
        keys: ['text'], 
        includeScore: true, 
        threshold: 0.4,
      };
      const fuse = new Fuse(data, options);
      const result = fuse.search(transcript)
      console.log(result);
      if (result.length > 0) {
        setIsOK(true)
      }
    }
  }, [transcript]);

    const startListening = async () => {
    // Start listening
    SpeechRecognition.startListening({ continuous: true , language: "it-IT"});
    setIsListening(true);

    // Wait for 7 seconds while listening
    await delay(9000);

    // Stop listening after 7 seconds
    SpeechRecognition.stopListening();
    setIsListening(false);
    resetTranscript()
    setIsOK(false)
  };

  const onBack=()=>{
    
    if((index-(indexBack))>0){
      setBack(true);
    }else{
      setBack(false);
    }
    setIndexBack(indexBack+1);
  }

  const fetchDataFromBackend = async () => {
    setLoading(true); // Imposta lo stato di caricamento
    try {
      let data = await verseLoader(title);
      setLoading(false); 
      if(!record){
        
        for (let i = 0; i < data.length+indexBackRef.current; i++) {
          if((i-indexBackRef.current)>=0){
            setBack(true);
          }else{
            setBack(false);
          }
          let indexCurr = (i-indexBackRef.current)>=0?(i-indexBackRef.current):0;
          setText(data[indexCurr].word);  
          setIndex(indexCurr);
          const voiceUrl = await downloadWorldUrl(title,data[indexCurr].word);
          setAudioSrc(voiceUrl);
          await delay(3000);
          await startListening();
        }
        setBack(false);
        setIndexBack(0)
      }
      const audioUrl = await downloadMusicUrl(title);
      setAudioSrc(audioUrl);
      let previousTime = 0; 
      
      for (let i = 0; i < data.length; i++) {
        setText(data[i].wordsToDisplay);
        console.log('qui'+i)
        setIndex(i);
        if(i+1!=data.length){
          let delayTime=data[i+1].time_word-previousTime
          console.log("time_word "+data[i+1].time_word);

          console.log("delayTime "+delayTime);
          console.log("previousTime "+previousTime);

          await delay(delayTime*1000);
          previousTime=data[i+1].time_word;
        }
      }
     
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
              {isListening && (
              <HStack>
                <Spinner color='red.500' />
                <Text>Sto controllando la pronuncia...</Text>
                  {isOK && (
                    <FcOk />
                  )}
              </HStack>
              )}
              {isRecording && (
                <HStack><Text>Canta tu ora!! Sto registrando </Text></HStack>
              )
              }
              {!isRecording && (
                <HStack><Text>Ripeti le parole che ascolti</Text></HStack>
              )
              }
              <ImageSlider
                index={index}
                title={title}
                text={text}
              ></ImageSlider>
              <AudioPlayer
                autoPlay
                src={audioSrc}
                onPlay={(e) => 
                  {
                    if(record){
                      if (stopRecordingBtnRef.current) {
                        startRecordingBtnRef.current.click()
                      }
                    }
                    console.log("onPlay")
                  }
                }
                onEnded={(e)=>{
                    if(record){
                      if (stopRecordingBtnRef.current) {
                        stopRecordingBtnRef.current.click()
                      }
                    }
                  }
                
                
              }
                showJumpControls={false}
                showDownloadProgress={false}
                showFilledProgress={false}
                customControlsSection={[
                  RHAP_UI.VOLUME_CONTROLS,
                ]}
                customProgressBarSection={
                    [
                      RHAP_UI.CURRENT_TIME,
                      <div>/</div>,
                      RHAP_UI.DURATION
                    ]
                }
                />
<div style={{ position: 'absolute', bottom: 200, left: 500, zIndex: 10, width:400 }}>
<ReactMediaRecorder
        video
        audio
       

        onStop={(blobUrl) => {
          const a = document.createElement('a');
          a.href = blobUrl;
          a.download = 'webcam-recording.webm';
          a.click();
        }}
        render={({ status, startRecording, stopRecording, mediaBlobUrl }) => (
          <div>
            
            <Button colorScheme="blue" onClick={startRecording} 
             style={{ display:  'none' }} ref={startRecordingBtnRef} 
            >
                        Start Recording
                      </Button>
                      <Button colorScheme="red" onClick={stopRecording}
                      style={{ display:  'none' }} ref={stopRecordingBtnRef} 
                      >
                        Stop Recording
                      </Button>  
          </div>
          
        )}
      />
</div>

            </Box>
          )}
        </ModalBody>
        <ModalFooter>
        {isBack ? (
          <Button bg="buttonCustom" color="white" marginRight="5" onClick={
            onBack}>
            Torna indietro
          </Button>
        ):""}
          <Button bg="buttonCustom" color="white" onClick={
            onClose}>
            Chiudi
          </Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}

import axios from "axios";
const apiUrl = import.meta.env.VITE_API_URL;

async function downloadMusicUrl(title) {
  const url = `${apiUrl}/api/files/?type=mp3&title=` + title;

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
    `${apiUrl}/api/files/?type=sentence&title=` +
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
  const url = `${apiUrl}/api/verse/?title=` + title;

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

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
