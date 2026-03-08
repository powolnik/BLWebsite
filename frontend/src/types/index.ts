export interface User {
  id: number; username: string; email: string; first_name: string; last_name: string;
  phone: string; avatar: string | null; bio: string; role: 'client' | 'member' | 'admin';
  company: string; website: string; date_joined: string;
}
export interface AuthTokens { access: string; refresh: string; }

export interface TeamMember {
  id: number; name: string; role: string; bio: string; photo: string;
  email: string; instagram: string; linkedin: string; behance: string; order: number;
}
export interface Festival {
  id: number; name: string; location: string; website: string;
  logo: string | null; description: string; project_count: number;
}
export interface ProjectImage { id: number; image: string; caption: string; is_cover: boolean; order: number; }
export interface ProjectListItem {
  id: number; title: string; slug: string; short_description: string; festival_name: string;
  date: string; category: string; is_featured: boolean; cover_image: string | null;
}
export interface ProjectDetail extends Omit<ProjectListItem, 'festival_name' | 'cover_image'> {
  description: string; festival: Festival | null; client: string; video_url: string;
  technologies: string; images: ProjectImage[]; testimonials: Testimonial[]; created_at: string;
}
export interface Testimonial {
  id: number; author: string; role: string; content: string; avatar: string | null;
  project_title: string; rating: number; created_at: string;
}

// === CONFIGURATOR ===
export interface SceneTemplate {
  id: number; name: string; slug: string; description: string; base_price: string;
  image_url: string; width: string; depth: string; height: string;
}
export interface ComponentCategory {
  id: number; name: string; slug: string; icon: string; color: string;
  description: string; order: number; components: SceneComponent[];
}
export interface SceneComponent {
  id: number; name: string; slug: string; description: string; short_desc: string;
  price: string; image_url: string; icon_name: string; color: string;
  category: number; category_name: string; category_color: string;
  width_m: string; depth_m: string;
  specs: Record<string, unknown>;
  power_consumption: number; weight_kg: string;
  is_available: boolean; max_quantity: number;
}

// Local scene item (not yet sent to API)
export interface SceneItem {
  id: string; // local UUID
  component: SceneComponent;
  quantity: number;
}

export interface OrderItem {
  id: number; component: number; component_name: string; component_icon: string; component_color: string;
  quantity: number; unit_price: string; subtotal: string;
  position_data: Record<string, unknown>; notes: string;
}
export interface SceneOrder {
  id: number; template: SceneTemplate | null; template_name?: string; status: string;
  event_name: string; event_date: string; event_end_date: string | null;
  event_location: string; expected_audience: number; subtotal: string;
  template_price: string; discount: string; total_price: string;
  notes: string; scene_data: Record<string, unknown>; items: OrderItem[];
  item_count?: number; created_at: string; updated_at: string;
}

// === SHOP ===
export interface ProductCategory {
  id: number; name: string; slug: string; description: string; image: string | null;
  parent: number | null; product_count: number; children: ProductCategory[];
}
export interface ProductListItem {
  id: number; name: string; slug: string; short_description: string; price: string;
  compare_price: string | null; category_name: string; primary_image: string | null;
  is_in_stock: boolean; is_featured: boolean;
}
export interface ProductDetail extends Omit<ProductListItem, 'category_name' | 'primary_image'> {
  description: string; sku: string; stock: number; weight_kg: string; tags: string;
  category: ProductCategory;
  images: { id: number; image: string; alt_text: string; is_primary: boolean; order: number }[];
  created_at: string;
}
export interface CartItem {
  id: number; product: number; product_name: string; product_price: string;
  product_image: string | null; quantity: number; subtotal: string;
}
export interface Cart { id: number; items: CartItem[]; total: string; item_count: number; updated_at: string; }
export interface ShopOrder {
  id: number; status: string; total: string; shipping_cost: string; discount: string;
  grand_total: string; shipping_name: string; shipping_street: string; shipping_city: string;
  shipping_postal_code: string; shipping_country: string; tracking_number: string; notes: string;
  items: { id: number; product_name: string; quantity: number; unit_price: string; subtotal: string }[];
  created_at: string;
}
export interface PaginatedResponse<T> { count: number; next: string | null; previous: string | null; results: T[]; }
