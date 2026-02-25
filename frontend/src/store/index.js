import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';

const store = configureStore({
    reducer: {
        auth: authReducer,
        // Les autres slices seront ajoutés par chaque membre :
        // quiz: quizReducer,       // M2
        // resources: resourcesReducer, // M2
        // feed: feedReducer,       // M1
        // messages: messagesReducer,   // M3
        // search: searchReducer,   // M4
        // profile: profileReducer, // M4
    },
});

export default store;
