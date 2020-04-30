--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.10
-- Dumped by pg_dump version 9.6.10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: _address; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._address (
    restaurant_id smallint,
    street character varying(18) DEFAULT NULL::character varying,
    zipcode smallint,
    city character varying(9) DEFAULT NULL::character varying,
    state character varying(2) DEFAULT NULL::character varying,
    country character varying(3) DEFAULT NULL::character varying,
    phone_number character varying(13) DEFAULT NULL::character varying,
    email character varying(26) DEFAULT NULL::character varying
);


ALTER TABLE public._address OWNER TO arjunsaikrishnan;

--
-- Name: _dietary; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._dietary (
    food_id character varying(1) DEFAULT NULL::character varying,
    category character varying(1) DEFAULT NULL::character varying
);


ALTER TABLE public._dietary OWNER TO arjunsaikrishnan;

--
-- Name: _menu; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._menu (
    food_id smallint,
    restaurant_id smallint,
    food character varying(33) DEFAULT NULL::character varying,
    unit_price numeric(4,2) DEFAULT NULL::numeric,
    category character varying(22) DEFAULT NULL::character varying,
    description character varying(165) DEFAULT NULL::character varying,
    discount character varying(3) DEFAULT NULL::character varying,
    new_price character varying(5) DEFAULT NULL::character varying,
    quantity character varying(3) DEFAULT NULL::character varying
);


ALTER TABLE public._menu OWNER TO arjunsaikrishnan;

--
-- Name: _order_join; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._order_join (
    order_id character varying(6) DEFAULT NULL::character varying,
    qrcode character varying(1) DEFAULT NULL::character varying,
    user_id smallint
);


ALTER TABLE public._order_join OWNER TO arjunsaikrishnan;

--
-- Name: _order_table; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._order_table (
    food_id smallint,
    new_price numeric(3,2) DEFAULT NULL::numeric,
    quantity smallint,
    food character varying(20) DEFAULT NULL::character varying,
    order_id character varying(6) DEFAULT NULL::character varying,
    confirmed smallint,
    user_id smallint
);


ALTER TABLE public._order_table OWNER TO arjunsaikrishnan;

--
-- Name: _restaurant_accounts; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._restaurant_accounts (
    restaurant_id smallint,
    username character varying(7) DEFAULT NULL::character varying,
    password character varying(8) DEFAULT NULL::character varying,
    email character varying(5) DEFAULT NULL::character varying
);


ALTER TABLE public._restaurant_accounts OWNER TO arjunsaikrishnan;

--
-- Name: _restaurants; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._restaurants (
    restaurant_id smallint,
    restaurant_name character varying(15) DEFAULT NULL::character varying,
    about character varying(352) DEFAULT NULL::character varying
);


ALTER TABLE public._restaurants OWNER TO arjunsaikrishnan;

--
-- Name: _sqlite_sequence; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._sqlite_sequence (
    name character varying(12) DEFAULT NULL::character varying,
    seq smallint
);


ALTER TABLE public._sqlite_sequence OWNER TO arjunsaikrishnan;

--
-- Name: _user_account; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._user_account (
    user_id smallint,
    username character varying(4) DEFAULT NULL::character varying,
    password character varying(8) DEFAULT NULL::character varying,
    email character varying(11) DEFAULT NULL::character varying
);


ALTER TABLE public._user_account OWNER TO arjunsaikrishnan;

--
-- Name: _user_accounts; Type: TABLE; Schema: public; Owner: arjunsaikrishnan
--

CREATE TABLE public._user_accounts (
    user_id smallint,
    username character varying(4) DEFAULT NULL::character varying,
    password character varying(8) DEFAULT NULL::character varying,
    email character varying(5) DEFAULT NULL::character varying
);


ALTER TABLE public._user_accounts OWNER TO arjunsaikrishnan;

--
-- Data for Name: _address; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._address (restaurant_id, street, zipcode, city, state, country, phone_number, email) FROM stdin;
1	19 Chambers Street	8542	Princeton	NJ	USA	(609)608-0104	contact@chennaichimney.com
\.


--
-- Data for Name: _dietary; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._dietary (food_id, category) FROM stdin;
\.


--
-- Data for Name: _menu; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._menu (food_id, restaurant_id, food, unit_price, category, description, discount, new_price, quantity) FROM stdin;
1	1	Tomato Shorba	5.95	Soups	Flavorful Soup made with tomatoes and Indian spices.	0.6	2.38	0
2	1	Sweet Corn Veg	6.95	Soups	Sweet corn, vegetables	0.4	4.17	0
3	1	Kozhi Milagu Charu	8.95	Soups	Chicken soup flavored with south Indian herbs and spices.	0.6	3.58	1
4	1	Aattukal Soup(Paya)	8.95	Soups	A refreshing medium spiced goat bone stock simmered with garlic, peppercorn and coriander finished with chettinadu spices.			
5	1	Marina Salad	7.95	From the Field	The Chennai beach style salad of chickpeas, mango, coconut, carrot & scallions tempered with mild spices.			
6	1	Curried Caesar Salad	6.95	From the Field	Crunchy romaine lettuce, plum tomatoes, cottage cheese tossed in curried caesar dressing, topped with crisps. -Choice of shrimp($4.00) or Chicken tikka($3.00) extra-	0.4	4.17	131
7	1	Moong bean salad	6.95	From the Field	Bean sprouts, scallions, carrots, coconut chips with cilantro, lime and feta crumbs.			
8	1	Street Samosa	6.95	Small Bites	Tri-folded puff pastry with potatoes, chilies, mint, cilantro and chat masala. (Vegan)	0.3	4.87	0
9	1	Kaaigari Pakoda	6.95	Small Bites	South Indian version of seasonal vegetable fritters. (Vegan)			
10	1	Veg Spring Roll	6.95	Small Bites	Crispy roll with vegetable filling			
11	1	Okra Karuku Muruku	8.95	Small Bites	Crispy fried okra. (Vegan)			
12	1	Kaalan Manchurian	9.95	Small Bites	Our very own recipe of mushrooms in dry Manchurian sauce Chennai style.			
13	1	Paneer Bajji	9.95	Small Bites	Paneer fritters served with chutney			
14	1	Paneer Tikka Multani	10.95	Small Bites	Cottage cheese, multi flour battered & grilled in tandoor.			
15	1	Chili Paneer	10.95	Small Bites	Indian cottage cheese tossed in hot chili sauce with onions and green bell peppers.			
16	1	Gobi Manchurian	10.95	Small Bites	Fresh florets of cauliflower battered, fried and cooked with bell pepper, onion and manchurian sauce Chinese style.			
17	1	Gobi-65	10.95	Small Bites	Fresh florets of cauliflower marinated in house spice and deep fried.			
18	1	Masala Idly	11.95	Small bites	Mildly spiced sauteed dish made from idli and tossed in Curry Leaves and South Indian spices.			
19	1	Kozhi 65	9.95	Small Bites	Cubes of chicken marinated in yogurt and spices, deep fried.			
20	1	Chicken Lollypop	11.95	Small Bites	Chicken wings marinated in chef\\'s special masala and deeep fried.			
21	1	Chicken Pepper Fry	10.95	Small Bites	Boneless chicken cooked with grounded pepper and onions.			
22	1	Chili Chicken	10.95	Small Bites	Deep fried chicken pieces tossed in a chili sauce with onions and green bell peppers.			
23	1	Murg Til Tikka	10.95	Small Bites	Sesame coated Tandoori barbecued chunks of chicken served with chutney and relish.			
24	1	Madurai Chukka Kari	11.95	Small Bites	Boneless lamb dry cooked in traditional masala a la Madurai style.			
25	1	Fish-65	10.95	Small Bites	Fish marinated in spicy masala and deep fried.			
26	1	Shrimp-65	11.95	Small Bites	Juicy shrimp marinated in special south Indian style masala and deep fried.			
27	1	Jeenga a Aatish	12.95	Small bites	Plump fresh jumbo prawns refreshingly marinated in citrus juice, ajwain and green cardamom, grilled in tandoor.			
28	1	Aloo Gobi Mutter Masala	12.95	Mains - Vegetarian	South Indian style gravy made with Potato, Cauliflower and Peas			
29	1	Kadai Sabzi	11.95	Mains - Vegetarian	Seasonal vegetables tossed with peppers, onions, tomatoes, crushed coriander.			
30	1	Ennai Kathirikai	12.95	Mains - Vegetarian	baby eggplant, roasted spices, tomatoes, onions, coconut paste.	0.1	11.65	10
31	1	Malai(Paneer) Koftha	13.95	Mains - Vegetarian	Gravy made with rich cream potato and paneer dumplings			
32	1	Vendakkai Masala	12.95	Mains - Vegetarian	Okra sauteed with onion, tomatoes, roasted ground spices.			
33	1	Kaalan Pattani Milagu Curry	12.95	Mains - Vegetarian	Button mushrooms, green peas in a spicy black pepper sauce.			
34	1	Navaratan Korma	12.95	Mains - Vegetarian	Rich aromatic curry made with medley of vegetables.			
35	1	Palak Tandoor Paneer	13.95	Mains - Vegetarian	Tandoori cooked cottage cheese simmered in cumin tempered sinach gravy, cream.			
36	1	Paneer Tikka Masala	13.95	Mains - Vegetarian	Grilled paneer cubes, onion and bell peppers served with creamy gravy with Indian spices.			
37	1	Paneer Butter Masala	13.95	Mains - Vegetarian	Rich, creamy and delicious paneer dish prepared using butter.			
38	1	Vegetable Chettinad	13.95	Mains - Vegetarian	Seasonal mix vegetable cooked with coconut paste and traditional chettinadu masala.			
39	1	Vegetable Kurma	13.95	Mains - Vegetarian	Seasonal mix vegetables cooked with coconut paste and spices.			
40	1	Old Delhi Butter Chicken	14.95	Mains - Poultry & Lamb	Pulled tandoori chicken cooked in butter, tomato sauce, aromatic spices.			
41	1	Milagu Kozhi Chettinad	15.95	Mains - Poultry & Lamb	Succulent pieces of bone-in chicken cooked in authentic Chettinad pepper gravy.			
42	1	Chennai Kozhi Curry	15.95	Mains - Poultry & Lamb	Boneless chicken curry made with fresh coriander, shallots, curry, leaves, pepper and yogurt.			
43	1	Murg Tikka Masala	15.95	Mains - Poultry & Lamb	Cubes of chicken char grilled and cooked in a tomato creamy sauce.			
44	1	Chicken Vindaloo	15.95	Mains - Poultry & Lamb	Boneless chicken and potato cooked with hot and tangy sauce			
45	1	Nilgiri Lamb Kurma	17.95	Mains - Poultry & Lamb	Cubes of lamb slowly simmered in coconut, fresh herbs & spices.			
46	1	Kashmiri Lamb Roganjosh	18.95	Mains - Poultry & Lamb	Chunks of lamb slow cooked in an onion, tomato, kashmiri red chili sauce.			
47	1	Lamb Vindaloo	18.95	Mains - Poultry & Lamb	Chunks of lamb and potato cooked in hot and tangy sauce.			
48	1	Lamb Chettinadu	18.95	Mains - Poultry & Lamb	Soft tender chunks of lamb cooked with south Indian style onion tomato gravy and Chettinad spices.			
49	1	Aattiraichi Varutha Araicha Curry	18.95	Mains - Poultry & Lamb	Traditional lamb curry cooked in roasted spices, a specialty from the town of Virudhunagar south India.			
50	1	Meen Varuval	18.95	Seafood	Fish delicately marinated in chili and lemon spice in south Indian style.			
51	1	Goan Fish Curry	18.95	Seafood	Fresh catch of the day cooked in coconut, malt vinegar, ground spices and kokum.			
52	1	Karaikudi Fish Curry	19.95	Seafood	Fish cooked in grounded spice gravy			
53	1	Yeral Thokku	19.95	Seafood	Prawn dry masala cooked with chef exotic spices			
54	1	Malabar Shrimp Curry	19.95	Seafood	Shrimp cooked in Malabar style			
55	1	Malai Murg Kabab	13.95	Clay Oven Char-Grilled	Chunks of chicken flavored with cream cheese, sour cream, pepper, lemon juice and cooked in tandoor clay oven.			
56	1	Chicken Seekh Kabab	14.95	Clay Oven Char-Grilled	Blended tender rolls of minced chicken, chopped onion, ginger, garlic and spices cooked in tandoor clay oven.			
57	1	Hariyali Murg Tikka	13.95	Clay Oven Char-Grilled	Tender boneless chicken breast cubes marinated with yogurt, spinach, mint leaves and cooked in tandoor clay oven.			
58	1	Whole Tandoori Chicken	18.95	Clay Oven Char-Grilled	Chicken marinated in yogurt, seasoned with spices and cooked in tandoor clay oven.			
59	1	Half Tandoori Chicken	13.95	Clay Oven Char-Grilled	Chicken marinated in yogurt, seasoned with spices and cooked in tandoori clay oven.			
60	1	Peshwari Boti Kabab	16.95	Clay Oven Char-Grilled	Lamb marinated in green papaya, red chili & ginger garlic paste, grilled in tandoor.			
61	1	Lamb Seek Kabab	18.95	Clay Oven Char-Grilled	Blended tender rolls of minced lamb, chopped onion, ginger, garlic and spices cooked in tandoor clay oven.			
62	1	Tandoori Lamb Chops	18.95	Clay Oven Char-Grilled	Baby lamb chops marinated in fresh ginger and garlic cooked to your taste.			
63	1	Mahi Tandoori	17.95	Clay Oven Char-Grilled	Fish marinated with garlic, lemon juice, ginger and garam masala and grilled in tandoor clay oven.			
64	1	Tandoori Pomfret	18.95	Clay Oven Char-Grilled	Fresh marinated Tandoor Pomfret in a spicy sauce and cooked on skewer in tandoor with mesquite charcoal.			
65	1	Bollywood Grill	23.95	Sizzlers & Platters	A combination kababs offer an ultimate sampler served with chutney and relishes.			
66	1	Naan	3.00	Breads	Choice of Butter/Onion/Mint			
67	1	Garlic or Cheese Mix Naan	3.75	Breads	Choice of Garlic/Cheese			
68	1	Bullet Naan	3.25	Breads	Naan with chopped chilies, cilantro			
69	1	Kashmiri Naan	3.75	Breads	Naan stuffed with coconut, nuts, dry fruits.			
70	1	Assorted Bread Basket	8.00	Breads	Choice of three breads. Onion Naan/Plain Naan/Garlic Naan/Roti/Butter Naan.			
71	1	Roti	3.00	Breads	Wheat bread.			
72	1	Plain/Mint Lacha Paratha	3.75	Breads	Layered wheat bread cooked in tandoor.			
73	1	Malabar Parota	5.99	Breads	Layered refined flour bread cooked in tawa.			
74	1	Vegetable Biryani	12.95	Biryanis	Aromatic basmati rice with seasonal vegetables infused with mild spices and saffron.			
75	1	Chicken Biryani	15.95	Biryanis	The perfect delicacy choicest cuts of chicken dum cooked with yogurt, golden fried onions, spices and saffron hued basmati rice.			
76	1	Lamb Biryani	17.95	Biryanis	The perfect delicacy choicest cuts of meat dum cooked with yogurt, golden fried onions, spices and saffron hued basmati rice.			
77	1	Masala Pappad	3.95	Sides	Large papad, tomato, onion, cilantro, green chilies, cucumber, lime & chaat spices.			
78	1	Cucumber Raitha	2.95	Sides	Yogurt with cucumber, mint and roasted cumin.			
79	1	Tadka Dal	9.95	Sides	Tempered yellow lentils with ginger, tomato and fresh coriander.			
80	1	Chennai Sambhar	5.95	Sides	Tempered yellow lentils with ground spices, seasonal vegetables, fresh coriander, curry leaves and clarified butter.			
81	1	Steamed rice	3.95	Sides	Basmati rice.			
82	1	Dahi	1.95	Sides	Plain Yogurt			
83	1	Madurai Idly	5.95	Chennai Specials	Spongy steamed rice cakes served hot with sambhar & chutneys. (Vegan)			
84	1	Sambhar Idly	6.95	Chennai Specials	Spongy steamed rice cakes served immersed in mildly spiced sambhar. (Vegan)	0.4	4.17	12
85	1	Idly Vada	7.95	Chennai Specials	Spongy steamed rice cakes and deep fried lentil doughnut served with sambhar and chutneys. (Vegan)			
86	1	Medhu Vada	5.95	Chennai Specials	South Indian deep fried lentil doughnuts served with chutneys. (Vegan)			
87	1	Sambhar Vada	6.95	Chennai Specials	South Indian deep fried lentil doughnut immersed in sambhar, onion & crisps. (Vegan)			
88	1	Plain Uthappam	9.95	Chennai Specials	Plain grilled pancake with chutney and sambar. Plain/Onion/Tomato/Carrots/Chilly			
89	1	Mix Veg. Uthappam	10.95	Chennai Specials	Pan grilled pancake topped with onion or tomatoes or carrots or chillies or mix served with chutney and sambhar.			
90	1	Plain Dosa	9.95	Chennai Specials	Crispy rice lentil crepe served with chutney and sambhar.			
91	1	Cone Dosa(for kids)	9.95	Chennai Specials				
92	1	Ghee Roast Dosa	10.95	Chennai Specials	Crispy rice lentil crepe roasted in clarified butter served with chutney and sambhar.			
93	1	Cheese Dosa	11.95	Chennai Specials	Crispy rice lentil crepe served with chutney and sambar.			
94	1	Chocolate Dosa (for kids)	10.95	Chennai Specials	Crispy rice lentil crepe topped with chocolate chips served with chutney and sambar.			
95	1	Podi/Kara Dosa	11.95	Chennai Specials	Crispy rice lentil crepe rubbed with spicy gun powder, spicy chutney, served with chutney and sambhar. (Podi Dosa / Kara Dosa)			
96	1	Masala Dosa	13.95	Chennai Specials	Crispy rice crepe stuffed with south Indian potato masala, served with chutneys & sambhar. (Masala Dosa / Mysore Masala Dosa)			
97	1	Mysore Masala Dosa	13.95	Chennai Specials	Crispy rice crepe stuffed with south Indian potato masala, served with chutneys & sambhar.			
98	1	Veg Manchurian Dosa	13.95	Chennai Specials	Crispy rice lentil crepe stuffed with manchurian, served with chutneys and sambhar.			
99	1	70mm Family Dosa	16.95	Chennai Specials	Long family size white lentil & rice crepe served with sambhar and chutney.			
100	1	Kal Dosa(Veg)	11.95	Chennai Specials	Thick rice lentil pancake served with choice of curry.			
101	1	Kal Dosa(chicken)	13.95	Chennai Specials	Thick rice lentil pancake served with choice of curry.			
102	1	Kal Dosa(lamb)	15.95	Chennai Specials	Thick rice lentil pancake served with choice of curry.			
103	1	Virudhunagar Chukakari dosa	15.95	Chennai Specials	Rice lentil crepe stuffed with lamb chunks cooked in onion spicy masala.			
104	1	Veg Kothu Parotta	11.95	Chennai Specials	Chopped layered bread cooked with vegetables, onion, tomatoes, chili, curry leaves and spices.			
105	1	Egg Kothu Parotta	11.95	Chennai Specials	Chopped layered bread cooked with vegetables, onion, tomatoes, chili, curry leaves and spices.			
106	1	Chicken Kothu Parotta	13.95	Chennai Specials	Flaky layered bread cooked with chicken curry masala.			
107	1	Malabar Parotta Salna(veg)	8.95	Chennai Specials	Layered bread cooked in Jawa served with vegetable salna.			
108	1	Malabar Parotta Salna(non-veg)	10.95	Chennai Specials	Layered bread cooked in Jawa served with choice of chicken or lamb salna.			
109	1	Srivilliputhur Palkova	7.95	Desserts	Sweet of reduced milk mildly flavoured with green cardamom, a rue speciality of Temple Town.			
110	1	Rasmalai	3.00	Desserts	Cheese soaked in sweet creamy syrup and topped with nuts.			
111	1	Gulab Jamun	3.00	Desserts	Dumplings of condensed milk deep fried and soaked in sugar syrup.			
112	1	Chilled Rice Pudding	3.00	Desserts	Rice, sweetened, saffron, vanilla bean			
113	1	Gajar Ka Halwa	3.95	Desserts	Freshly grated carrots, cooked in milk and topped with nuts.			
114	1	Flooda	7.95	Desserts	Ice cream, silky vermicelli and black basil seed steeped in flavored milk.			
\.


--
-- Data for Name: _order_join; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._order_join (order_id, qrcode, user_id) FROM stdin;
Pquqr9		1
lr90Ec		1
nU2ziE		1
5zJTbR		1
fW6Elf		1
Viw10s		1
utuOL3		1
I6DAPr		1
4FvKuF		1
iXjkxZ		1
WsStAZ		1
37cLhz		1
6e3Nbr		1
DjcbIH		1
vR6iQ7		1
tBUGr4		1
uLDfV0		1
tBImv0		1
MI0n8d		1
F29H7h		1
1J48GB		1
7igbOJ		1
z0FLSP		1
4PMJYI		1
		1
hTjSat		1
BfCoQZ		1
TveZFk		1
RLRcrh		1
PBAdtd		1
\.


--
-- Data for Name: _order_table; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._order_table (food_id, new_price, quantity, food, order_id, confirmed, user_id) FROM stdin;
6	4.17	5	Curried Caesar Salad	hTjSat	1	1
3	3.58	1	Kozhi Milagu Charu	BfCoQZ	1	1
6	4.17	1	Curried Caesar Salad	BfCoQZ	1	1
3	3.58	10	Kozhi Milagu Charu	TveZFk	1	1
6	4.17	1	Curried Caesar Salad	RLRcrh	1	1
6	4.17	1	Curried Caesar Salad	PBAdtd	1	1
\.


--
-- Data for Name: _restaurant_accounts; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._restaurant_accounts (restaurant_id, username, password, email) FROM stdin;
1	chennai	password	email
\.


--
-- Data for Name: _restaurants; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._restaurants (restaurant_id, restaurant_name, about) FROM stdin;
1	Chennai Chimney	Set in the historic town of Princeton, New Jersey, Chennai Chimney, an Indian restaurant, offers exotic dishes in authentic flavor from the traditional kitchens of Southern India where the city of Chennai is located. Our contemporary version of rustic Indian food will be beyond your expectations and take you on a mouthwatering journey to its origins.
\.


--
-- Data for Name: _sqlite_sequence; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._sqlite_sequence (name, seq) FROM stdin;
user_account	1
\.


--
-- Data for Name: _user_account; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._user_account (user_id, username, password, email) FROM stdin;
1	user	password	h@gmail.com
\.


--
-- Data for Name: _user_accounts; Type: TABLE DATA; Schema: public; Owner: arjunsaikrishnan
--

COPY public._user_accounts (user_id, username, password, email) FROM stdin;
1	user	password	email
\.


--
-- PostgreSQL database dump complete
--

