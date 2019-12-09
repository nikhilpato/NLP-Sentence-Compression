import React from 'react';
import styles from './Header.module.css';

function Header() {
    return (
        <div className={styles.header_container}>
            <div className={styles.title_container}>
                Sentence Compression Project:
            </div>
            <div className={styles.text_container}>
                This project is focused on being able to take a sentence and compressing 
                it to the main subject of the whole sentence. The resultant output sentence 
                must be grammatically correct while still maintaining the information from 
                the original sentence. 
                The impact of this project is that it could easily compress large documents 
                to be able to either search them quickly or to make a document have less text 
                to read in general.
            </div>
            <div className={styles.title_container}>
                How to Use:
            </div>
            <div className={styles.text_container}>
                Enter a sentence of any length in the textbox below and click submit.  
                We will then take your sentence and reduce the length of it, showing 
                only the main subject of the sentence. The output sentence is expected 
                to be grammatically correct.
            </div>
        </div>
    )
}

export default Header;