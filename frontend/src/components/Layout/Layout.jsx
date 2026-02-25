import { Outlet } from 'react-router-dom';
import Navbar from '../Navbar/Navbar';
import Sidebar from '../Sidebar/Sidebar';
import './Layout.css';

/**
 * Layout principal de l'application (Navbar + Sidebar + contenu).
 * Utilisé pour les routes protégées (après connexion).
 */
const Layout = () => {
    return (
        <div className="app-layout">
            <Navbar />
            <div className="app-body">
                <Sidebar />
                <main className="app-content">
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;
