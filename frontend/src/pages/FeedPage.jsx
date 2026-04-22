import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import communityService from '../services/communityService';

function FeedPage() {
  const { user } = useSelector((state) => state.auth);
  const [feed, setFeed] = useState({ suggestions: [], posts: [], matches: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [postDraft, setPostDraft] = useState('');

  const loadFeed = async () => {
    setLoading(true);
    setError('');
    try {
      const data = await communityService.getFeed();
      setFeed(data);
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Impossible de charger le feed.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFeed();
  }, []);

  const handleSwipe = async (candidateId, direction) => {
    try {
      await communityService.swipe(candidateId, direction);
      await loadFeed();
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Swipe impossible.');
    }
  };

  const handlePostSubmit = async (event) => {
    event.preventDefault();
    if (!postDraft.trim()) {
      return;
    }
    try {
      await communityService.createPost({
        content: postDraft,
        course: 'Communaute',
        tags: ['tinamu', 'campus'],
      });
      setPostDraft('');
      await loadFeed();
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Publication impossible.');
    }
  };

  return (
    <div className="page-stack">
      <section className="hero-card gradient-card">
        <div>
          <p className="eyebrow">Feed campus</p>
          <h1>Salut {user?.prenom || 'toi'}, la communaute tourne pour de vrai.</h1>
          <p>
            Suggestions d'entraide, posts de promo et matchs reciproques sont tous
            alimentes par l'API locale.
          </p>
        </div>
        <div className="hero-metrics">
          <article>
            <strong>{feed.suggestions.length}</strong>
            <span>profils a decouvrir</span>
          </article>
          <article>
            <strong>{feed.matches.length}</strong>
            <span>matchs reciproques</span>
          </article>
          <article>
            <strong>{feed.posts.length}</strong>
            <span>posts visibles</span>
          </article>
        </div>
      </section>

      {error ? <p className="status-error">{error}</p> : null}

      <div className="content-grid content-grid-wide">
        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Nouveau post</span>
            <h2>Partage un tip utile</h2>
          </div>
          <form className="composer" onSubmit={handlePostSubmit}>
            <textarea
              value={postDraft}
              onChange={(event) => setPostDraft(event.target.value)}
              placeholder="Exemple: j'ai publie une checklist API security dans les ressources."
              rows="4"
            />
            <button type="submit" className="btn-primary">
              Publier
            </button>
          </form>
        </section>

        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Matchs</span>
            <h2>Etudiants deja connectes</h2>
          </div>
          <div className="chips-row">
            {feed.matches.length ? (
              feed.matches.map((match) => (
                <span key={match.id} className="chip">
                  {match.prenom} {match.nom} · {match.badge}
                </span>
              ))
            ) : (
              <p className="muted-text">Aucun match pour l'instant, mais le terrain est ouvert.</p>
            )}
          </div>
        </section>
      </div>

      <div className="content-grid">
        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Swipe intelligent</span>
            <h2>Profils recommandes</h2>
          </div>
          {loading ? <p className="muted-text">Chargement des suggestions...</p> : null}
          <div className="list-grid">
            {feed.suggestions.map((candidate) => (
              <article key={candidate.id} className="profile-card">
                <div className="profile-card-header">
                  <span className="avatar-large">{candidate.prenom?.[0]}</span>
                  <div>
                    <h3>{candidate.prenom} {candidate.nom}</h3>
                    <p>{candidate.niveau} · {candidate.specialite}</p>
                  </div>
                </div>
                <p>{candidate.bio}</p>
                <div className="chips-row">
                  <span className="chip chip-outline">{candidate.badge}</span>
                  <span className="chip chip-outline">{candidate.score_aide} pts aide</span>
                </div>
                <div className="action-row">
                  <button
                    type="button"
                    className="btn-secondary"
                    onClick={() => handleSwipe(candidate.id, 'left')}
                  >
                    Passer
                  </button>
                  <button
                    type="button"
                    className="btn-primary"
                    onClick={() => handleSwipe(candidate.id, 'right')}
                  >
                    Suivre
                  </button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Communaute</span>
            <h2>Derniers posts</h2>
          </div>
          <div className="timeline">
            {feed.posts.map((post) => (
              <article key={post.id} className="timeline-item">
                <div className="timeline-item-header">
                  <div>
                    <strong>{post.author.prenom} {post.author.nom}</strong>
                    <span>{post.course}</span>
                  </div>
                  <span className="pill">{post.tags.join(' · ')}</span>
                </div>
                <p>{post.content}</p>
                <div className="meta-row">
                  <span>{post.likes} likes</span>
                  <span>{post.comments} commentaires</span>
                </div>
              </article>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

export default FeedPage;
