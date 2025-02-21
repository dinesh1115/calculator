import React, { useState } from "react";
import { View, Text, TextInput, Button, StyleSheet, Alert } from "react-native";
import axios from "axios";

const API_URL = "http://192.168.1.104:8000/calculate"; // Add "/calculate"



const App: React.FC = () => {
  const [num1, setNum1] = useState<string>("");
  const [num2, setNum2] = useState<string>("");
  const [result, setResult] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCalculation = async (operation: string) => {
    if (!num1 || !num2) {
      Alert.alert("Error", "Please enter both numbers.");
      return;
    }

    try {
      const response = await axios.post(API_URL, {
        num1: parseFloat(num1),
        num2: parseFloat(num2),
        operation,
      });

      if (response.data.error) {
        setError(response.data.error);
        setResult(null);
      } else {
        setResult(response.data.result);
        setError(null);
      }
    } catch (err) {
      setError("Error connecting to backend");
      setResult(null);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Simple Calculator</Text>

      <TextInput
        style={styles.input}
        placeholder="Enter first number"
        keyboardType="numeric"
        value={num1}
        onChangeText={setNum1}
      />
      <TextInput
        style={styles.input}
        placeholder="Enter second number"
        keyboardType="numeric"
        value={num2}
        onChangeText={setNum2}
      />

      <View style={styles.buttonContainer}>
        <Button title="Add" onPress={() => handleCalculation("add")} />
        <Button title="Subtract" onPress={() => handleCalculation("subtract")} />
        <Button title="Multiply" onPress={() => handleCalculation("multiply")} />
        <Button title="Divide" onPress={() => handleCalculation("divide")} />
      </View>

      {result !== null && <Text style={styles.result}>Result: {result}</Text>}
      {error && <Text style={styles.error}>{error}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#f0f0f0",
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: "bold",
    marginBottom: 20,
  },
  input: {
    width: "80%",
    height: 40,
    borderColor: "#ccc",
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
    backgroundColor: "#fff",
    borderRadius: 5,
  },
  buttonContainer: {
    flexDirection: "row",
    justifyContent: "space-between",
    width: "80%",
    marginTop: 10,
  },
  result: {
    fontSize: 20,
    marginTop: 20,
    color: "green",
  },
  error: {
    fontSize: 16,
    marginTop: 10,
    color: "red",
  },
});

export default App;
