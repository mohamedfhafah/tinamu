import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import ProtectedRoute from './components/ProtectedRoute';
import MessagesPage from './components/Messages/MessagesPage';
import SearchPage from './components/Search/SearchPage';

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
  return (
    <BrowserRouter>
      <Routes>
        {/* Route publique */}
        <Route path="/login" element={<div>Login — à implémenter</div>} />

        {/* Routes protégées avec layout */}
        <Route element={<ProtectedRoute />}>
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate to="/feed" replace />} />
            <Route path="/feed" element={<div>Feed — à implémenter</div>} />
            <Route path="/quiz" element={<div>Quiz — à implémenter</div>} />
            <Route path="/resources" element={<div>Ressources — à implémenter</div>} />
            <Route path="/messages" element={<MessagesPage />} />
            <Route path="/search" element={<SearchPage />} />
            <Route path="/profile" element={<div>Profil — à implémenter</div>} />
          </Route>
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
