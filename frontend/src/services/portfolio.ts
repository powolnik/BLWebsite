import api from './api';
import type { TeamMember, ProjectListItem, ProjectDetail, Festival, Testimonial, PaginatedResponse } from '../types';

export const portfolioService = {
  getTeam: async (): Promise<TeamMember[]> => (await api.get('/portfolio/team/')).data,
  getFestivals: async (): Promise<PaginatedResponse<Festival>> => (await api.get('/portfolio/festivals/')).data,
  getProjects: async (params?: { category?: string; is_featured?: boolean; search?: string; page?: number }): Promise<PaginatedResponse<ProjectListItem>> =>
    (await api.get('/portfolio/projects/', { params })).data,
  getProject: async (slug: string): Promise<ProjectDetail> => (await api.get(`/portfolio/projects/${slug}/`)).data,
  getTestimonials: async (): Promise<Testimonial[]> => (await api.get('/portfolio/testimonials/')).data,
};
