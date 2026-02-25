import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import MessagesPage from './components/Messages/MessagesPage';
import SearchPage from './components/Search/SearchPage';
import Login from './pages/Login/Login';
import Register from './pages/Register/Register';
import NotFound from './pages/NotFound/NotFound';
import Feed from './pages/Feed/Feed';
import ErrorPage from './pages/ErrorPage/ErrorPage';

/**
 * App — Configuration du routing principal.
 *
 * Routes publiques :
 *   /login        → Page Login (M1)
 *   /register     → Page Inscription (M1)
 *
 * Routes protégées (via ProtectedRoute) :
 *   /feed         → Feed Tinder (M1)
 *   /quiz         → Quiz (M2)
 *   /resources    → Ressources (M2)
 *   /messages     → Messagerie (M3)
 *   /search       → Recherche (M3)
 *   /profile      → Profil (M4)
 *
 * Erreurs :
 *   /404          → Page 404
 *   *             → Redirect vers /login
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Routes publiques (M1) */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/404" element={<NotFound />} />
        <Route path="/error" element={<ErrorPage />} />

        {/* Routes protégées avec layout */}
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate to="/feed" replace />} />
            <Route path="/feed" element={<Feed />} />
            <Route path="/quiz" element={<div>Quiz — à implémenter (M2)</div>} />
            <Route path="/resources" element={<div>Ressources — à implémenter (M2)</div>} />
            <Route path="/messages" element={<MessagesPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/profile" element={<div>Profil — à implémenter (M4)</div>} />
          </Route>
        </Route>

        {/* Fallback */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
