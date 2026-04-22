import { useEffect, useState } from 'react';
import communityService from '../services/communityService';

function MessagesPage() {
  const [conversations, setConversations] = useState([]);
  const [activeId, setActiveId] = useState('');
  const [activeConversation, setActiveConversation] = useState(null);
  const [draft, setDraft] = useState('');
  const [error, setError] = useState('');

  const loadConversations = async () => {
    try {
      const data = await communityService.getConversations();
      setConversations(data);
      if (!activeId && data.length) {
        setActiveId(data[0].id);
      }
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Impossible de charger les conversations.');
    }
  };

  useEffect(() => {
    loadConversations();
  }, []);

  useEffect(() => {
    if (!activeId) {
      return;
    }
    const loadConversation = async () => {
      try {
        const data = await communityService.getConversation(activeId);
        setActiveConversation(data);
      } catch (requestError) {
        setError(requestError.response?.data?.message || 'Conversation introuvable.');
      }
    };
    loadConversation();
  }, [activeId]);

  const handleSend = async (event) => {
    event.preventDefault();
    if (!draft.trim()) {
      return;
    }
    try {
      await communityService.sendMessage(activeId, draft);
      setDraft('');
      await loadConversations();
      const refreshed = await communityService.getConversation(activeId);
      setActiveConversation(refreshed);
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Envoi impossible.');
    }
  };

  return (
    <div className="page-stack">
      <section className="hero-card card">
        <div className="section-heading">
          <span className="eyebrow">Messaging</span>
          <h1>Conversations de promo branchees au backend.</h1>
        </div>
        <p>
          Les threads et messages sont exposes via l'API locale, puis rendus dans une vue
          double panneau pour une demo plus credible.
        </p>
      </section>

      {error ? <p className="status-error">{error}</p> : null}

      <section className="card split-layout">
        <aside className="conversation-list">
          <div className="section-heading compact">
            <span className="eyebrow">Inbox</span>
            <h2>Threads</h2>
          </div>
          {conversations.map((conversation) => {
            const names = conversation.participants
              .map((participant) => participant.prenom)
              .join(', ');
            return (
              <button
                key={conversation.id}
                type="button"
                className={`conversation-item ${activeId === conversation.id ? 'active' : ''}`}
                onClick={() => setActiveId(conversation.id)}
              >
                <strong>{names}</strong>
                <span>{conversation.last_message?.body || 'Aucun message'}</span>
              </button>
            );
          })}
        </aside>

        <div className="conversation-panel">
          {activeConversation ? (
            <>
              <div className="conversation-header">
                <h2>
                  {activeConversation.participants
                    .map((participant) => `${participant.prenom} ${participant.nom}`)
                    .join(' · ')}
                </h2>
              </div>
              <div className="messages-list">
                {activeConversation.messages.map((message) => (
                  <article key={message.id} className="message-bubble">
                    <strong>{message.author.prenom}</strong>
                    <p>{message.body}</p>
                  </article>
                ))}
              </div>
              <form className="toolbar" onSubmit={handleSend}>
                <input
                  value={draft}
                  onChange={(event) => setDraft(event.target.value)}
                  placeholder="Envoyer un message utile"
                />
                <button type="submit" className="btn-primary">
                  Envoyer
                </button>
              </form>
            </>
          ) : (
            <p className="muted-text">Selectionne une conversation pour commencer.</p>
          )}
        </div>
      </section>
    </div>
  );
}

export default MessagesPage;
