import React, { useState, useCallback } from 'react';
import { Form, Field } from 'react-final-form';
import axios from 'axios';
import styles from './Content.module.css';

/**
 *----------------------------------------
 * App Content Component
 *----------------------------------------
 *
 * This component contains the main 
 * application content along with all 
 * the required functionality
 * 
 *----------------------------------------
 */

function Content() {
    const [data, setData] = useState({ response: [] });

    /**
     * onSubmit
     * 
     * When the user inputs a sentence, this function 
     * sends a request to compress it.
     * @param {*} e 
     */
    const onSubmit = (e)=> {
        compress('http://3.17.25.67:9090/' + e.sentence)
    };

    /**
     * useCallback
     * 
     * This is the acutal API request. Sends the request
     * and recieves the reponse.
     */
    const compress = useCallback(async (url) => { 
            axios.get(url)
                .then(res => {
                    setData({ response: res.data })
                }
            )
        },
        [],
    )

    /**
     * getCompression
     * 
     * Formats the sentence once the data has been 
     * recieved from the API. Words that are removed
     * are red, while those that are kept are black.
     * This is displayed in teh compression section.
     */
    const getCompression = () => {
        const sentence = []
        for (const idx in data.response) {
            const element = data.response[idx]
            sentence.push(<div key={element} style={{ paddingRight: '4px', 
                                color: element.keep ? 'black' : 'red'}}>{element.word}</div>)
        }
        return sentence
    }

    /**
     * getResult
     * 
     * Formats the sentence once the data has been 
     * recieved form the API. Removes all the words
     * that are removed by the sentence compression model.
     * This is displayed in the result section.
     */
    const getResult = () => {
        const sentence = []
        for (const idx in data.response) {
            const element = data.response[idx]
            if (element.keep)
                sentence.push(<div key={element} style={{paddingRight:'4px'}}>{element.word}</div>)
        }
        return sentence
    }

    /* // component declarations */
    return(
        <div className={styles.content_container}>

            { /* // Sentence Section */ }
            <Form
                onSubmit={ onSubmit}
                render={({ handleSubmit }) => (
                    <div className={styles.input_container} >
                        <form onSubmit={handleSubmit} className={styles.form_container}>
                            <label className={styles.label_name}> Sentence </label>
                            <Field className={styles.text_field}
                                name='sentence' 
                                component='input' 
                                type='text'
                                placeholder='Input Sentence...' 
                            />
                            <button className={styles.submit_button} type='submit'>Compress</button> 
                        </form>
                    </div>
                )}
            />

            { /* // Sentence Section */ }
            <div className={styles.process_container}>
                <div className={styles.label_name}>
                    Compression
                </div>
                <div className={styles.sub_container}>
                    <div className={styles.words}>
                        {getCompression()}
                    </div>
                </div>
            </div>

            { /* // Sentence Section */ }
            <div className={styles.results_container}>
                <div className={styles.label_name}>
                    Result
                </div>
                <div className={styles.sub_container}>
                    <div className={styles.words}>
                        {getResult()}
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Content;
