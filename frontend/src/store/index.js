import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import messagingReducer from './slices/messagingSlice';
import searchReducer from './slices/searchSlice';

const store = configureStore({
    reducer: {
        auth: authReducer,
        messaging: messagingReducer,   // M3
        search: searchReducer,         // M3
        // quiz: quizReducer,          // M2
        // resources: resourcesReducer, // M2
        // feed: feedReducer,          // M1
        // profile: profileReducer,    // M4
    },
});

export default store;
