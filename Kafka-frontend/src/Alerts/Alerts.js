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
