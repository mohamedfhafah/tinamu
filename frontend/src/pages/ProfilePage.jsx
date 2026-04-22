import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useParams } from 'react-router-dom';
import authService from '../services/authService';
import communityService from '../services/communityService';
import { fetchMe } from '../store/slices/authSlice';

function ProfilePage() {
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const { userId } = useParams();
  const activeUserId = userId || user?.id;
  const [profileData, setProfileData] = useState(null);
  const [stats, setStats] = useState(null);
  const [form, setForm] = useState({
    bio: '',
    specialite: '',
    avatar_url: '',
  });
  const [error, setError] = useState('');

  const loadProfile = async () => {
    if (!activeUserId) {
      return;
    }
    try {
      const [profilePayload, statsPayload] = await Promise.all([
        communityService.getProfile(activeUserId),
        communityService.getProfileStats(activeUserId),
      ]);
      setProfileData(profilePayload);
      setStats(statsPayload);

      if (profilePayload.relationship.is_self) {
        setForm({
          bio: profilePayload.user.bio || '',
          specialite: profilePayload.user.specialite || '',
          avatar_url: profilePayload.user.avatar_url || '',
        });
      }
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Chargement du profil impossible.');
    }
  };

  useEffect(() => {
    loadProfile();
  }, [activeUserId]);

  const handleSave = async (event) => {
    event.preventDefault();
    try {
      await authService.updateMe(form);
      await dispatch(fetchMe());
      await loadProfile();
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Mise a jour impossible.');
    }
  };

  const toggleFollow = async () => {
    if (!profileData || profileData.relationship.is_self) {
      return;
    }
    try {
      if (profileData.relationship.is_following) {
        await communityService.unfollowUser(profileData.user.id);
      } else {
        await communityService.followUser(profileData.user.id);
      }
      await loadProfile();
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Action impossible.');
    }
  };

  if (!profileData || !stats) {
    return <p className="muted-text">Chargement du profil...</p>;
  }

  const { user: profile, relationship } = profileData;

  return (
    <div className="page-stack">
      <section className="hero-card gradient-card">
        <div className="profile-hero">
          <span className="avatar-hero">{profile.prenom?.[0]}</span>
          <div>
            <p className="eyebrow">{profile.badge}</p>
            <h1>{profile.prenom} {profile.nom}</h1>
            <p>{profile.niveau} · {profile.specialite || 'Specialite a definir'}</p>
          </div>
        </div>
        <div className="hero-metrics">
          <article>
            <strong>{stats.followers}</strong>
            <span>followers</span>
          </article>
          <article>
            <strong>{stats.following}</strong>
            <span>following</span>
          </article>
          <article>
            <strong>{stats.score_quiz + stats.score_aide}</strong>
            <span>score global</span>
          </article>
        </div>
      </section>

      {error ? <p className="status-error">{error}</p> : null}

      <div className="content-grid">
        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Bio</span>
            <h2>Presentation</h2>
          </div>
          <p>{profile.bio || 'Pas encore de bio renseignee.'}</p>
          {!relationship.is_self ? (
            <button type="button" className="btn-primary" onClick={toggleFollow}>
              {relationship.is_following ? 'Ne plus suivre' : 'Suivre ce profil'}
            </button>
          ) : null}
        </section>

        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Stats</span>
            <h2>Signal de progression</h2>
          </div>
          <div className="stat-list">
            <div>
              <strong>{stats.score_aide}</strong>
              <span>score aide</span>
            </div>
            <div>
              <strong>{stats.score_quiz}</strong>
              <span>score quiz</span>
            </div>
            <div>
              <strong>{stats.badge}</strong>
              <span>badge dominant</span>
            </div>
          </div>
        </section>
      </div>

      {relationship.is_self ? (
        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Edition</span>
            <h2>Mettre a jour le profil</h2>
          </div>
          <form className="form-stack" onSubmit={handleSave}>
            <label className="field">
              <span>Specialite</span>
              <input
                value={form.specialite}
                onChange={(event) =>
                  setForm((current) => ({ ...current, specialite: event.target.value }))
                }
              />
            </label>
            <label className="field">
              <span>Avatar URL</span>
              <input
                value={form.avatar_url}
                onChange={(event) =>
                  setForm((current) => ({ ...current, avatar_url: event.target.value }))
                }
              />
            </label>
            <label className="field">
              <span>Bio</span>
              <textarea
                rows="4"
                value={form.bio}
                onChange={(event) =>
                  setForm((current) => ({ ...current, bio: event.target.value }))
                }
              />
            </label>
            <button type="submit" className="btn-primary">
              Sauvegarder
            </button>
          </form>
        </section>
      ) : null}
    </div>
  );
}

export default ProfilePage;
