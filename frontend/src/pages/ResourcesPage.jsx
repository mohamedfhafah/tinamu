import { useEffect, useState } from 'react';
import communityService from '../services/communityService';

function ResourcesPage() {
  const [resources, setResources] = useState([]);
  const [query, setQuery] = useState('');
  const [form, setForm] = useState({
    title: '',
    type: 'Lien',
    course: 'General',
    description: '',
    tags: '',
    url: '',
  });
  const [error, setError] = useState('');

  const loadResources = async (search = '') => {
    try {
      const data = await communityService.getResources({ q: search });
      setResources(data);
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Impossible de charger les ressources.');
    }
  };

  useEffect(() => {
    loadResources();
  }, []);

  const handleSearch = async (event) => {
    event.preventDefault();
    await loadResources(query);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await communityService.addResource(form);
      setForm({
        title: '',
        type: 'Lien',
        course: 'General',
        description: '',
        tags: '',
        url: '',
      });
      await loadResources(query);
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Ajout impossible.');
    }
  };

  return (
    <div className="page-stack">
      <section className="hero-card card">
        <div className="section-heading">
          <span className="eyebrow">Knowledge layer</span>
          <h1>Ressources partagees, filtrables et extensibles.</h1>
        </div>
        <p>
          Cette brique montre le flow d'une bibliotheque interne: recherche, listing, et
          ajout d'une ressource depuis le frontend.
        </p>
      </section>

      {error ? <p className="status-error">{error}</p> : null}

      <div className="content-grid">
        <section className="card">
          <form className="toolbar" onSubmit={handleSearch}>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Chercher par cours, mot-cle ou stack"
            />
            <button type="submit" className="btn-secondary">
              Filtrer
            </button>
          </form>

          <div className="list-grid">
            {resources.map((resource) => (
              <article key={resource.id} className="resource-card">
                <div className="resource-card-top">
                  <div>
                    <strong>{resource.title}</strong>
                    <span>{resource.course} · {resource.type}</span>
                  </div>
                  <a href={resource.url} target="_blank" rel="noreferrer" className="pill">
                    Ouvrir
                  </a>
                </div>
                <p>{resource.description}</p>
                <div className="chips-row">
                  {resource.tags.map((tag) => (
                    <span key={tag} className="chip chip-outline">
                      {tag}
                    </span>
                  ))}
                </div>
                <small>Ajoute par {resource.author}</small>
              </article>
            ))}
          </div>
        </section>

        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Nouvelle ressource</span>
            <h2>Ajout rapide</h2>
          </div>
          <form className="form-stack" onSubmit={handleSubmit}>
            <label className="field">
              <span>Titre</span>
              <input
                value={form.title}
                onChange={(event) => setForm((current) => ({ ...current, title: event.target.value }))}
              />
            </label>
            <label className="field">
              <span>Cours</span>
              <input
                value={form.course}
                onChange={(event) => setForm((current) => ({ ...current, course: event.target.value }))}
              />
            </label>
            <label className="field">
              <span>Type</span>
              <input
                value={form.type}
                onChange={(event) => setForm((current) => ({ ...current, type: event.target.value }))}
              />
            </label>
            <label className="field">
              <span>Description</span>
              <textarea
                rows="3"
                value={form.description}
                onChange={(event) =>
                  setForm((current) => ({ ...current, description: event.target.value }))
                }
              />
            </label>
            <label className="field">
              <span>Tags</span>
              <input
                value={form.tags}
                onChange={(event) => setForm((current) => ({ ...current, tags: event.target.value }))}
                placeholder="react, api, security"
              />
            </label>
            <label className="field">
              <span>URL</span>
              <input
                value={form.url}
                onChange={(event) => setForm((current) => ({ ...current, url: event.target.value }))}
                placeholder="https://..."
              />
            </label>
            <button type="submit" className="btn-primary">
              Ajouter
            </button>
          </form>
        </section>
      </div>
    </div>
  );
}

export default ResourcesPage;
