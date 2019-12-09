import React from 'react';
import Header from '../Header/Header';
import Content from '../Content/Content';
import styles from './App.module.css';


/**
 *----------------------------------------
 * Main App Component
 *----------------------------------------
 *
 * This is the main application that 
 * contains the header and the sentence 
 * compression content.
 *
 *----------------------------------------
 */

function App() {
  return (
    <div className={styles.app_container}>
      <div className={styles.header_container}>
        <Header />
      </div>
      <div className={styles.content_container}>
        <Content />
      </div>
    </div>
  );
}

export default App;
