import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { clearError, login } from '../store/slices/authSlice';

const demoAccounts = [
  {
    label: 'Cyber',
    identifier: 'clara.lefebvre@etu.univ.fr',
    password: 'TinAMU2026!',
    helper: 'L2 cybersecurite',
  },
  {
    label: 'DevOps',
    identifier: 'giulia.romano@etu.univ.fr',
    password: 'TinAMU2026!',
    helper: 'M1 cloud & devops',
  },
  {
    label: 'Mentor',
    identifier: 'hugo.lambert@etu.univ.fr',
    password: 'TinAMU2026!',
    helper: 'M2 securite informatique',
  },
];

function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isAuthenticated, loading, error } = useSelector((state) => state.auth);
  const [formData, setFormData] = useState({
    identifier: demoAccounts[0].identifier,
    password: demoAccounts[0].password,
  });

  useEffect(() => {
    if (isAuthenticated) {
      navigate('/feed', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  useEffect(() => () => {
    dispatch(clearError());
  }, [dispatch]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const result = await dispatch(login(formData));
    if (!result.error) {
      navigate('/feed', { replace: true });
    }
  };

  const quickLogin = async (account) => {
    setFormData({ identifier: account.identifier, password: account.password });
    const result = await dispatch(
      login({ identifier: account.identifier, password: account.password })
    );
    if (!result.error) {
      navigate('/feed', { replace: true });
    }
  };

  return (
    <div className="login-shell">
      <section className="login-hero">
        <p className="eyebrow">Campus social platform prototype</p>
        <h1>Un hub etudiant propre, testable et vraiment vivant.</h1>
        <p className="login-copy">
          TinAMU connecte mentorat, quiz, ressources et conversations pour les etudiants
          en informatique. Cette demo locale tourne avec un backend Flask + React et un
          jeu de donnees seedes pour faciliter la verification.
        </p>

        <div className="stats-grid">
          <article className="stat-card">
            <strong>9</strong>
            <span>profils actifs</span>
          </article>
          <article className="stat-card">
            <strong>3</strong>
            <span>parcours demo</span>
          </article>
          <article className="stat-card">
            <strong>6</strong>
            <span>modules relies</span>
          </article>
        </div>

        <div className="demo-cards">
          {demoAccounts.map((account) => (
            <button
              key={account.identifier}
              type="button"
              className="demo-card"
              onClick={() => quickLogin(account)}
            >
              <span className="demo-card-label">{account.label}</span>
              <strong>{account.identifier}</strong>
              <span>{account.helper}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="login-panel">
        <div className="panel-glow" />
        <form className="login-form card" onSubmit={handleSubmit}>
          <div className="section-heading">
            <span className="eyebrow">Connexion demo</span>
            <h2>Reconnecte-toi au campus</h2>
          </div>

          <label className="field">
            <span>Email universitaire</span>
            <input
              type="email"
              value={formData.identifier}
              onChange={(event) =>
                setFormData((current) => ({ ...current, identifier: event.target.value }))
              }
              placeholder="prenom.nom@etu.univ.fr"
            />
          </label>

          <label className="field">
            <span>Mot de passe</span>
            <input
              type="password"
              value={formData.password}
              onChange={(event) =>
                setFormData((current) => ({ ...current, password: event.target.value }))
              }
              placeholder="TinAMU2026!"
            />
          </label>

          {error ? <p className="status-error">{error}</p> : null}

          <button type="submit" className="btn-primary" disabled={loading}>
            {loading ? 'Connexion...' : 'Entrer dans TinAMU'}
          </button>

          <div className="muted-block">
            <p>Compte seed recommande:</p>
            <code>clara.lefebvre@etu.univ.fr / TinAMU2026!</code>
          </div>
        </form>
      </section>
    </div>
  );
}

export default LoginPage;
