 import React, { JSX } from 'react';
 import Layout from '@theme-init/Layout';
 import Chatbot from '../components/Chatbot'; // Import your Chatbot component
 
 export default function MyLayout(props: { children: React.ReactNode }): JSX.Element {
   return (
     <Layout {...props}>
       {props.children}
       <Chatbot /> {/* Render the Chatbot component */}
        </Layout>
      );
    }