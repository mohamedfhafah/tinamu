import api from './api';

const communityService = {
  getFeed: async () => {
    const response = await api.get('/feed');
    return response.data;
  },

  swipe: async (userId, direction) => {
    const response = await api.post('/feed/swipe', {
      user_id: userId,
      direction,
    });
    return response.data;
  },

  createPost: async (payload) => {
    const response = await api.post('/feed/posts', payload);
    return response.data;
  },

  getQuizzes: async () => {
    const response = await api.get('/quiz');
    return response.data;
  },

  getQuiz: async (quizId) => {
    const response = await api.get(`/quiz/${quizId}`);
    return response.data;
  },

  submitQuiz: async (quizId, answers) => {
    const response = await api.post(`/quiz/${quizId}/submit`, { answers });
    return response.data;
  },

  getLeaderboard: async () => {
    const response = await api.get('/quiz/leaderboard');
    return response.data;
  },

  getResources: async (params = {}) => {
    const response = await api.get('/resources', { params });
    return response.data;
  },

  addResource: async (payload) => {
    const response = await api.post('/resources', payload);
    return response.data;
  },

  getConversations: async () => {
    const response = await api.get('/conversations');
    return response.data;
  },

  getConversation: async (conversationId) => {
    const response = await api.get(`/conversations/${conversationId}/messages`);
    return response.data;
  },

  sendMessage: async (conversationId, body) => {
    const response = await api.post(`/conversations/${conversationId}/messages`, { body });
    return response.data;
  },

  createConversation: async (userId) => {
    const response = await api.post('/conversations', { user_id: userId });
    return response.data;
  },

  searchUsers: async (params = {}) => {
    const response = await api.get('/search/users', { params });
    return response.data;
  },

  getProfile: async (userId) => {
    const response = await api.get(`/profile/${userId}`);
    return response.data;
  },

  getProfileStats: async (userId) => {
    const response = await api.get(`/profile/${userId}/stats`);
    return response.data;
  },

  followUser: async (userId) => {
    const response = await api.post(`/profile/${userId}/follow`);
    return response.data;
  },

  unfollowUser: async (userId) => {
    const response = await api.delete(`/profile/${userId}/follow`);
    return response.data;
  },
};

export default communityService;
