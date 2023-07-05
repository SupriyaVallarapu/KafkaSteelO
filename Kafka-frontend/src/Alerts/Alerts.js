import React from 'react';
import Alert from 'react-bootstrap/Alert';

export function SuccessfulUploadAlert({ onClose }) {
    return <Alert variant="success" onClose={onClose} dismissible>Data uploaded successfully!</Alert>;
}

export function FailedUploadAlert({ onClose }) {
    return <Alert variant="danger" onClose={onClose} dismissible>Failed to upload data.</Alert>;
}

export function EmptyFieldAlert({ onClose }) {
    return <Alert variant="warning" onClose={onClose} dismissible>All fields must be filled out!</Alert>;
}

export function DirectoryPathDoesntExistAlert({ onClose }) {
    return <Alert variant="warning" onClose={onClose} dismissible>The directory folder path doesn't exist!</Alert>;
}

export function URLAlert({ onClose }) {
    return <Alert variant="warning" onClose={onClose} dismissible> Error during URL call</Alert>
}

export function NoFilesInPathAlert({ onClose }) {
    return <Alert variant="info" onClose={onClose} dismissible>No files are present in the provided directory.</Alert>;
}

export function RequestBodyErrorAlert({ onClose }) {
    return <Alert variant="warning" onClose={onClose} dismissible>Error parsing request body.</Alert>;
}

export function DBConnectionErrorAlert({ onClose }) {
    return <Alert variant="danger" onClose={onClose} dismissible>Error connecting to database.</Alert>;
}

export function CreateTableErrorAlert({ onClose }) {
    return <Alert variant="danger" onClose={onClose} dismissible>Error creating table.</Alert>;
}

export function TopicNotFoundErrorAlert({ onClose }) {
    return <Alert variant="danger" onClose={onClose} dismissible>Topic not found in Kafka.</Alert>;
}


export function UnexpectedErrorAlert({ onClose }) {
    return <Alert variant="danger" onClose={onClose} dismissible>An unknown error occurred.</Alert>;
}

export function OpcuaURLconnectAlert({onClose}){
    return <Alert variant="warning" onClose={onClose} dismissible>Could not connect to URL </Alert>
}

export function CannotConnectToBrokerAlert({onClose}){
    return <Alert variant='danger' onClose={onClose} dismissible>Unable to connect to Kafka broker</Alert>
}
