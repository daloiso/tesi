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
            <Text >Caricato</Text> 
          )}
        </ModalBody>
        <ModalFooter>
          <Button bg="buttonCustom"  color="white" onClick={onClose}>Close</Button>
        </ModalFooter>
      </ModalContent>
    </Modal>
  );
}