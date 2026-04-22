import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import communityService from '../services/communityService';

function SearchPage() {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [niveau, setNiveau] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState('');

  const search = async (nextQuery = '', nextNiveau = '') => {
    try {
      const data = await communityService.searchUsers({ q: nextQuery, niveau: nextNiveau });
      setResults(data);
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Recherche impossible.');
    }
  };

  useEffect(() => {
    search();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    await search(query, niveau);
  };

  return (
    <div className="page-stack">
      <section className="hero-card card">
        <div className="section-heading">
          <span className="eyebrow">Directory</span>
          <h1>Recherche multi-critere sur les profils campus.</h1>
        </div>
        <p>
          Ici on expose une vraie route de recherche, utile pour montrer le catalogue
          d'utilisateurs et le rebond vers le profil detaille.
        </p>
      </section>

      {error ? <p className="status-error">{error}</p> : null}

      <section className="card">
        <form className="toolbar" onSubmit={handleSubmit}>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Nom, specialite, email..."
          />
          <select value={niveau} onChange={(event) => setNiveau(event.target.value)}>
            <option value="">Tous les niveaux</option>
            <option value="L1">L1</option>
            <option value="L2">L2</option>
            <option value="L3">L3</option>
            <option value="M1">M1</option>
            <option value="M2">M2</option>
          </select>
          <button type="submit" className="btn-primary">
            Chercher
          </button>
        </form>

        <div className="list-grid">
          {results.map((result) => (
            <article key={result.id} className="profile-card">
              <div className="profile-card-header">
                <span className="avatar-large">{result.prenom?.[0]}</span>
                <div>
                  <h3>{result.prenom} {result.nom}</h3>
                  <p>{result.niveau} · {result.specialite}</p>
                </div>
              </div>
              <p>{result.bio}</p>
              <div className="chips-row">
                <span className="chip">{result.badge}</span>
                <span className="chip chip-outline">{result.score_quiz} quiz</span>
              </div>
              <button
                type="button"
                className="btn-secondary"
                onClick={() => navigate(`/profile/${result.id}`)}
              >
                Voir le profil
              </button>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}

export default SearchPage;
