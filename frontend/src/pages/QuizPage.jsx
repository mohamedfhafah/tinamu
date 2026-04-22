import { useEffect, useState } from 'react';
import { useDispatch } from 'react-redux';
import { fetchMe } from '../store/slices/authSlice';
import communityService from '../services/communityService';

function QuizPage() {
  const dispatch = useDispatch();
  const [quizzes, setQuizzes] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [selectedQuizId, setSelectedQuizId] = useState('');
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const loadOverview = async () => {
    try {
      const [quizItems, board] = await Promise.all([
        communityService.getQuizzes(),
        communityService.getLeaderboard(),
      ]);
      setQuizzes(quizItems);
      setLeaderboard(board);
      if (!selectedQuizId && quizItems.length) {
        setSelectedQuizId(quizItems[0].id);
      }
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Impossible de charger les quiz.');
    }
  };

  useEffect(() => {
    loadOverview();
  }, []);

  useEffect(() => {
    if (!selectedQuizId) {
      return;
    }

    const loadQuiz = async () => {
      try {
        const quiz = await communityService.getQuiz(selectedQuizId);
        setSelectedQuiz(quiz);
        setAnswers({});
        setResult(null);
      } catch (requestError) {
        setError(requestError.response?.data?.message || 'Quiz introuvable.');
      }
    };

    loadQuiz();
  }, [selectedQuizId]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedQuiz) {
      return;
    }

    try {
      const payload = await communityService.submitQuiz(selectedQuiz.id, answers);
      setResult(payload);
      await loadOverview();
      dispatch(fetchMe());
    } catch (requestError) {
      setError(requestError.response?.data?.message || 'Soumission impossible.');
    }
  };

  return (
    <div className="page-stack">
      <section className="hero-card card">
        <div className="section-heading">
          <span className="eyebrow">Quiz engine</span>
          <h1>Un module de revision qui pousse aussi le leaderboard.</h1>
        </div>
        <p>
          Chaque soumission repasse par l'API, calcule un score et met a jour le profil
          courant. Pas de poudre aux yeux, juste un flow propre.
        </p>
      </section>

      {error ? <p className="status-error">{error}</p> : null}

      <div className="content-grid">
        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Catalogue</span>
            <h2>Choisis un quiz</h2>
          </div>
          <div className="list-grid">
            {quizzes.map((quiz) => (
              <button
                key={quiz.id}
                type="button"
                className={`select-card ${selectedQuizId === quiz.id ? 'selected' : ''}`}
                onClick={() => setSelectedQuizId(quiz.id)}
              >
                <strong>{quiz.title}</strong>
                <span>{quiz.topic} · {quiz.difficulty}</span>
                <small>{quiz.questions_count} questions · {quiz.estimated_minutes} min</small>
              </button>
            ))}
          </div>
        </section>

        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">Leaderboard</span>
            <h2>Top score campus</h2>
          </div>
          <ol className="leaderboard">
            {leaderboard.map((entry) => (
              <li key={entry.id}>
                <div>
                  <strong>{entry.prenom} {entry.nom}</strong>
                  <span>{entry.badge}</span>
                </div>
                <strong>{entry.score_quiz}</strong>
              </li>
            ))}
          </ol>
        </section>
      </div>

      {selectedQuiz ? (
        <section className="card">
          <div className="section-heading">
            <span className="eyebrow">{selectedQuiz.topic}</span>
            <h2>{selectedQuiz.title}</h2>
          </div>
          <p>{selectedQuiz.description}</p>

          <form className="form-stack" onSubmit={handleSubmit}>
            {selectedQuiz.questions.map((question, index) => (
              <fieldset key={question.id} className="question-card">
                <legend>{index + 1}. {question.prompt}</legend>
                {question.options.map((option) => (
                  <label key={option} className="radio-row">
                    <input
                      type="radio"
                      name={question.id}
                      checked={answers[question.id] === option}
                      onChange={() =>
                        setAnswers((current) => ({ ...current, [question.id]: option }))
                      }
                    />
                    <span>{option}</span>
                  </label>
                ))}
              </fieldset>
            ))}
            <button type="submit" className="btn-primary">
              Soumettre
            </button>
          </form>

          {result ? (
            <div className="result-banner">
              <strong>
                Score: {result.score}/{result.total}
              </strong>
              <span>+{result.gained_points} points quiz ajoutes au profil.</span>
            </div>
          ) : null}
        </section>
      ) : null}
    </div>
  );
}

export default QuizPage;
