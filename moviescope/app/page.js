'use client';

import React from 'react';
import { redirect } from 'next/navigation'


const WelcomePage = () => {

  const handleButtonClick = () => {
    redirect('/library');
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Welcome to MovieScope</h1>
      <button style={styles.button} onClick={handleButtonClick}>Enter Library</button>
    </div>
  );
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    textAlign: 'center',
    background: 'linear-gradient(135deg, #3b005d, #001f3f)', // Darker gradient background
    color: '#ffffff',
    fontFamily: '"Comic Sans MS", cursive, sans-serif',
  },
  title: {
    fontSize: '3em',
    marginBottom: '20px',
    color: '#ff71ce',
    textShadow: `
      0 0 10px #ff71ce, 
      0 0 20px #ff71ce, 
      0 0 30px #ff71ce, 
      0 0 40px #ff71ce, 
      0 0 50px #ff71ce`, // Stronger glow with multiple shadow layers
  },
  button: {
    padding: '12px 24px',
    fontSize: '1.2em',
    fontWeight: 'bold',
    color: '#00ffff',
    backgroundColor: 'transparent',
    border: '2px solid #00ffff',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    textShadow: `
      0 0 5px #00ffff, 
      0 0 10px #00ffff, 
      0 0 15px #00ffff`, // Slightly stronger glow for button text
  },
};

// Add hover effect
styles.button[':hover'] = {
  color: '#ff00ff',
  borderColor: '#ff00ff',
  textShadow: `
    0 0 5px #ff00ff, 
    0 0 10px #ff00ff, 
    0 0 15px #ff00ff`, // Increase glow intensity on hover
};

export default WelcomePage;
