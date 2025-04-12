// App.js
import React, { useState, useRef } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, Image, ScrollView, Alert } from 'react-native';
import { Camera } from 'expo-camera';
import * as ImagePicker from 'expo-image-picker';
import * as FileSystem from 'expo-file-system';
import axios from 'axios';

export default function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraVisible, setCameraVisible] = useState(false);
  const [capturedImage, setCapturedImage] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState(null);
  const cameraRef = useRef(null);

  React.useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({ quality: 0.8 });
      setCapturedImage(photo.uri);
      setCameraVisible(false);
    }
  };

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.8,
    });

    if (!result.cancelled && result.assets && result.assets[0].uri) {
      setCapturedImage(result.assets[0].uri);
    }
  };

  const processImage = async () => {
    if (!capturedImage) return;
    
    setProcessing(true);
    try {
      // Convert image to base64
      const base64Image = await FileSystem.readAsStringAsync(capturedImage, {
        encoding: FileSystem.EncodingType.Base64,
      });
      
      // Send to backend API
      const response = await axios.post('http://YOUR_BACKEND_API/process-image', {
        image: base64Image
      });
      
      setResults(response.data);
      Alert.alert('Success', 'Data extracted successfully!');
    } catch (error) {
      console.error('Error processing image:', error);
      Alert.alert('Error', 'Failed to process the image. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  const exportToExcel = async () => {
    if (!results) return;
    
    try {
      const response = await axios.post('http://YOUR_BACKEND_API/export-excel', {
        data: results
      }, {
        responseType: 'blob'
      });
      
      // Handle the downloaded file
      // In a real app, you'd save this to device storage
      Alert.alert('Success', 'Data exported to Excel successfully!');
    } catch (error) {
      console.error('Error exporting to Excel:', error);
      Alert.alert('Error', 'Failed to export data. Please try again.');
    }
  };

  if (hasPermission === null) {
    return <View style={styles.container}><Text>Requesting camera permission...</Text></View>;
  }
  if (hasPermission === false) {
    return <View style={styles.container}><Text>No access to camera</Text></View>;
  }

  return (
    <View style={styles.container}>
      {cameraVisible ? (
        <View style={styles.cameraContainer}>
          <Camera style={styles.camera} ref={cameraRef} type={Camera.Constants.Type.back}>
            <View style={styles.buttonContainer}>
              <TouchableOpacity style={styles.button} onPress={takePicture}>
                <Text style={styles.text}>Take Photo</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.button} onPress={() => setCameraVisible(false)}>
                <Text style={styles.text}>Cancel</Text>
              </TouchableOpacity>
            </View>
          </Camera>
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <Text style={styles.title}>Questionnaire Scanner</Text>
          
          {capturedImage && (
            <View style={styles.imageContainer}>
              <Image source={{ uri: capturedImage }} style={styles.previewImage} />
            </View>
          )}
          
          <View style={styles.buttonRow}>
            <TouchableOpacity style={styles.mainButton} onPress={() => setCameraVisible(true)}>
              <Text style={styles.buttonText}>Camera</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.mainButton} onPress={pickImage}>
              <Text style={styles.buttonText}>Gallery</Text>
            </TouchableOpacity>
          </View>
          
          {capturedImage && (
            <TouchableOpacity 
              style={[styles.processButton, processing && styles.disabledButton]} 
              onPress={processImage}
              disabled={processing}
            >
              <Text style={styles.buttonText}>
                {processing ? 'Processing...' : 'Process Image'}
              </Text>
            </TouchableOpacity>
          )}
          
          {results && (
            <View style={styles.resultsContainer}>
              <Text style={styles.resultsTitle}>Extracted Data:</Text>
              {Object.entries(results).map(([key, value]) => (
                <View key={key} style={styles.resultRow}>
                  <Text style={styles.resultLabel}>{key}:</Text>
                  <Text style={styles.resultValue}>{value}</Text>
                </View>
              ))}
              
              <TouchableOpacity style={styles.exportButton} onPress={exportToExcel}>
                <Text style={styles.buttonText}>Export to Excel</Text>
              </TouchableOpacity>
            </View>
          )}
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContainer: {
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginVertical: 20,
  },
  cameraContainer: {
    flex: 1,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'row',
    justifyContent: 'center',
    margin: 20,
    position: 'absolute',
    bottom: 0,
    width: '100%',
  },
  button: {
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 10,
    margin: 10,
  },
  text: {
    fontSize: 18,
    color: 'black',
  },
  imageContainer: {
    width: '100%',
    height: 300,
    marginVertical: 20,
    borderRadius: 10,
    overflow: 'hidden',
    elevation: 5,
  },
  previewImage: {
    width: '100%',
    height: '100%',
  },
  buttonRow: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
    marginBottom: 20,
  },
  mainButton: {
    backgroundColor: '#4285F4',
    padding: 15,
    borderRadius: 10,
    width: '45%',
    alignItems: 'center',
  },
  processButton: {
    backgroundColor: '#0F9D58',
    padding: 15,
    borderRadius: 10,
    width: '90%',
    alignItems: 'center',
  },
  disabledButton: {
    backgroundColor: '#cccccc',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
    fontWeight: 'bold',
  },
  resultsContainer: {
    width: '100%',
    backgroundColor: 'white',
    padding: 15,
    borderRadius: 10,
    marginTop: 20,
    elevation: 3,
  },
  resultsTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  resultRow: {
    flexDirection: 'row',
    paddingVertical: 5,
    borderBottomWidth: 1,
    borderBottomColor: '#eeeeee',
  },
  resultLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    width: '40%',
  },
  resultValue: {
    fontSize: 16,
    width: '60%',
  },
  exportButton: {
    backgroundColor: '#DB4437',
    padding: 15,
    borderRadius: 10,
    marginTop: 20,
    alignItems: 'center',
  },
});
