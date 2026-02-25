import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
    const menuItems = [
        { path: '/feed', icon: '🃏', label: 'Feed' },
        { path: '/quiz', icon: '🧠', label: 'Quiz' },
        { path: '/messages', icon: '💬', label: 'Messages' },
        { path: '/resources', icon: '📚', label: 'Ressources' },
        { path: '/search', icon: '🔍', label: 'Recherche' },
        { path: '/profile', icon: '👤', label: 'Profil' },
    ];

    return (
        <aside className="sidebar">
            <ul className="sidebar-menu">
                {menuItems.map((item) => (
                    <li key={item.path}>
                        <NavLink
                            to={item.path}
                            className={({ isActive }) =>
                                isActive ? 'sidebar-link active' : 'sidebar-link'
                            }
                        >
                            <span className="sidebar-icon">{item.icon}</span>
                            <span className="sidebar-label">{item.label}</span>
                        </NavLink>
                    </li>
                ))}
            </ul>
        </aside>
    );
};

export default Sidebar;
