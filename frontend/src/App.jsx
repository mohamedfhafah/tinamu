import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import FeedPage from './pages/FeedPage';
import QuizPage from './pages/QuizPage';
import ResourcesPage from './pages/ResourcesPage';
import MessagesPage from './pages/MessagesPage';
import SearchPage from './pages/SearchPage';
import ProfilePage from './pages/ProfilePage';
import { fetchMe } from './store/slices/authSlice';
import './pages/pages.css';

/**
 * App — Configuration du routing principal.
 *
 * Routes publiques :
 *   /login       → Page Login (M4)
 *
 * Routes protégées (via ProtectedRoute) :
 *   /feed        → Feed Tinder (M1)
 *   /quiz        → Quiz (M2)
 *   /resources   → Ressources (M2)
 *   /messages    → Messagerie (M3)
 *   /search      → Recherche (M3)
 *   /profile     → Profil (M4)
 */
function App() {
  const dispatch = useDispatch();
  const { isAuthenticated, user } = useSelector((state) => state.auth);

  useEffect(() => {
    if (isAuthenticated && !user) {
      dispatch(fetchMe());
    }
  }, [dispatch, isAuthenticated, user]);

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate to="/feed" replace />} />
            <Route path="/feed" element={<FeedPage />} />
            <Route path="/quiz" element={<QuizPage />} />
            <Route path="/resources" element={<ResourcesPage />} />
            <Route path="/messages" element={<MessagesPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/profile/:userId" element={<ProfilePage />} />
          </Route>
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
