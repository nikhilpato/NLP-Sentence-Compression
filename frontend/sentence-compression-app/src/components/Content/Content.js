import React, { useState, useCallback } from 'react';
import { Form, Field } from 'react-final-form';
import axios from 'axios';
import styles from './Content.module.css';

function Content() {
    const [data, setData] = useState({ response: [] });

    const onSubmit = (e)=> {
        compress('http://3.17.25.67:9090/' + e.sentence)
    };

    const compress = useCallback(async (url) => { 
            axios.get(url)
                .then(res => {
                    setData({ response: res.data })
                }
            )
        },
        [],
    )

    const getCompression = () => {
        const sentence = []
        for (const idx in data.response) {
            const element = data.response[idx]
            sentence.push(<div key={element} style={{ paddingRight: '4px', 
                                color: element.keep ? 'black' : 'red'}}>{element.word}</div>)
        }
        return sentence
    }

    const getResult = () => {
        const sentence = []
        for (const idx in data.response) {
            const element = data.response[idx]
            if (element.keep)
                sentence.push(<div key={element} style={{paddingRight:'4px'}}>{element.word}</div>)
        }
        return sentence
    }

    return(
        <div className={styles.content_container}>
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
