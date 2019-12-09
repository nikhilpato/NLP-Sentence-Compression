import React from 'react';
import Header from '../Header/Header';
import Content from '../Content/Content';
import styles from './App.module.css';

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
