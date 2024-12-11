import React, { useState, useEffect } from 'react';
import { 
  Modal, 
  ModalContent, 
  ModalHeader, 
  ModalCloseButton, 
  ModalBody, 
  Text, 
  ModalFooter, 
  Button, 
  ModalOverlay 
} from "@chakra-ui/react";
import AudioPlayer, {RHAP_UI} from 'react-h5-audio-player';
import 'react-h5-audio-player/lib/styles.css';
export default function Player({ isOpen, onClose, title }) {

  const [loading, setLoading] = useState(false);  
  
  useEffect(() => {
    if (isOpen) {
      // Quando il modal si apre, effettua la chiamata al backend
      fetchDataFromBackend();
    }
  }, [isOpen]);

  const fetchDataFromBackend = async () => {
    setLoading(true); // Imposta lo stato di caricamento
    try {
      //TODO
      console.log("prova")
    } catch (error) {
      console.error('Errore durante la chiamata al backend:', error);
    } finally {
      setLoading(false); // Dopo aver ricevuto i dati, ferma il caricamento
    }
  };


  const OverlayOne = () => (
    <ModalOverlay
      bg='none'
      backdropFilter='auto'
      backdropInvert='80%'
      backdropBlur='2px'
    />
  );


  return (
    <Modal isCentered isOpen={isOpen} onClose={onClose} >
      {OverlayOne()}
      <ModalContent bg="yellowCustom">
        <ModalHeader>{title}</ModalHeader>
        <ModalBody>
        {loading ? (
            <Text color="gray.500">Caricamento dei dati in corso...</Text>  // Messaggio di caricamento
          ) : (
            <AudioPlayer
                autoPlay
                src="http://example.com/audio.mp3"
                onPlay={e => console.log("onPlay")}
                showJumpControls={false}
                showDownloadProgress={false}
                showFilledProgress={false}
                customControlsSection={[
                    RHAP_UI.MAIN_CONTROLS,
                    RHAP_UI.VOLUME_CONTROLS,
                ]}
            />
          )}
        </ModalBody>
        <ModalFooter>
          <Button bg="buttonCustom"  color="white" onClick={onClose}>Close</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}