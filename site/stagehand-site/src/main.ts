import App from "./App.svelte";

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
	apiKey: "AIzaSyBU4mxUNld8umgxeVDjqi2Nxf7DlchwoQM",
	authDomain: "stagehand-4b847.firebaseapp.com",
	projectId: "stagehand-4b847",
	storageBucket: "stagehand-4b847.appspot.com",
	messagingSenderId: "662818689263",
	appId: "1:662818689263:web:cd808e32dfa2fb1c088b1a",
	measurementId: "G-ZXXHEK8V9W",
};

// Initialize Firebase
const appFirebase = initializeApp(firebaseConfig);
const analytics = getAnalytics(appFirebase);

const app = new App({
	target: document.body,
});

export default app;
