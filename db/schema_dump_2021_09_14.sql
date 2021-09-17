--
-- PostgreSQL database dump
--

-- Dumped from database version 12.8 (Debian 12.8-1.pgdg100+1)
-- Dumped by pg_dump version 12.8 (Ubuntu 12.8-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: fuzzystrmatch; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS fuzzystrmatch WITH SCHEMA public;


--
-- Name: EXTENSION fuzzystrmatch; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION fuzzystrmatch IS 'determine similarities and distance between strings';


--
-- Name: pg_stat_statements; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_stat_statements WITH SCHEMA public;


--
-- Name: EXTENSION pg_stat_statements; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION pg_stat_statements IS 'track execution statistics of all SQL statements executed';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: batters_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.batters_conference (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: batters_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.batters_conference_inseason (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: batters_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.batters_overall (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: batters_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.batters_overall_inseason (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: duplicate_names; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.duplicate_names (
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    id integer
);


--
-- Name: game_log; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.game_log (
    game_num integer NOT NULL,
    date date,
    season integer NOT NULL,
    team character varying(30) NOT NULL,
    opponent character varying(30),
    result character varying(1),
    rs integer,
    ra integer,
    home boolean,
    conference boolean
);


--
-- Name: game_log_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.game_log_inseason (
    scrape_date date NOT NULL,
    game_num integer NOT NULL,
    date date,
    season integer NOT NULL,
    team character varying(30) NOT NULL,
    opponent character varying(30),
    result character varying(1),
    rs integer,
    ra integer,
    home boolean,
    conference boolean
);


--
-- Name: league_offense_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.league_offense_overall (
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    lg_r_pa numeric,
    bsr_bmult numeric,
    bsr numeric,
    lw_hbp numeric,
    lw_bb numeric,
    lw_x1b numeric,
    lw_x2b numeric,
    lw_x3b numeric,
    lw_hr numeric,
    lw_sb numeric,
    lw_cs numeric,
    lw_out numeric,
    ww_hbp numeric,
    ww_bb numeric,
    ww_x1b numeric,
    ww_x2b numeric,
    ww_x3b numeric,
    ww_hr numeric,
    woba_scale numeric,
    woba numeric,
    sbr numeric,
    lg_wsb numeric,
    wsb numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    rep_level numeric,
    rar numeric
);


--
-- Name: guts; Type: VIEW; Schema: public; Owner: -
--

CREATE VIEW public.guts AS
 SELECT league_offense_overall.season,
    league_offense_overall.lg_r_pa,
    league_offense_overall.bsr_bmult,
    league_offense_overall.lw_hbp,
    league_offense_overall.lw_bb,
    league_offense_overall.lw_x1b,
    league_offense_overall.lw_x2b,
    league_offense_overall.lw_x3b,
    league_offense_overall.lw_hr,
    league_offense_overall.lw_sb,
    league_offense_overall.lw_cs,
    league_offense_overall.lw_out,
    league_offense_overall.ww_hbp,
    league_offense_overall.ww_bb,
    league_offense_overall.ww_x1b,
    league_offense_overall.ww_x2b,
    league_offense_overall.ww_x3b,
    league_offense_overall.ww_hr,
    league_offense_overall.woba_scale,
    league_offense_overall.rep_level
   FROM public.league_offense_overall;


--
-- Name: league_offense_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.league_offense_conference (
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    lg_r_pa numeric,
    bsr_bmult numeric,
    bsr numeric,
    lw_hbp numeric,
    lw_bb numeric,
    lw_x1b numeric,
    lw_x2b numeric,
    lw_x3b numeric,
    lw_hr numeric,
    lw_sb numeric,
    lw_cs numeric,
    lw_out numeric,
    ww_hbp numeric,
    ww_bb numeric,
    ww_x1b numeric,
    ww_x2b numeric,
    ww_x3b numeric,
    ww_hr numeric,
    woba_scale numeric,
    woba numeric,
    sbr numeric,
    lg_wsb numeric,
    wsb numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    rep_level numeric,
    rar numeric
);


--
-- Name: league_offense_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.league_offense_conference_inseason (
    season integer,
    date date NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    lg_r_pa numeric,
    bsr_bmult numeric,
    bsr numeric,
    lw_hbp numeric,
    lw_bb numeric,
    lw_x1b numeric,
    lw_x2b numeric,
    lw_x3b numeric,
    lw_hr numeric,
    lw_sb numeric,
    lw_cs numeric,
    lw_out numeric,
    ww_hbp numeric,
    ww_bb numeric,
    ww_x1b numeric,
    ww_x2b numeric,
    ww_x3b numeric,
    ww_hr numeric,
    woba_scale numeric,
    woba numeric,
    sbr numeric,
    lg_wsb numeric,
    wsb numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    rep_level numeric,
    rar numeric
);


--
-- Name: league_offense_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.league_offense_overall_inseason (
    season integer,
    date date NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    lg_r_pa numeric,
    bsr_bmult numeric,
    bsr numeric,
    lw_hbp numeric,
    lw_bb numeric,
    lw_x1b numeric,
    lw_x2b numeric,
    lw_x3b numeric,
    lw_hr numeric,
    lw_sb numeric,
    lw_cs numeric,
    lw_out numeric,
    ww_hbp numeric,
    ww_bb numeric,
    ww_x1b numeric,
    ww_x2b numeric,
    ww_x3b numeric,
    ww_hr numeric,
    woba_scale numeric,
    woba numeric,
    sbr numeric,
    lg_wsb numeric,
    wsb numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    rep_level numeric,
    rar numeric
);


--
-- Name: league_pitching_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.league_pitching_conference (
    season integer NOT NULL,
    g integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    hr integer,
    era numeric,
    ra_9 numeric,
    so_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric,
    raa numeric,
    era_minus numeric
);


--
-- Name: league_pitching_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.league_pitching_overall (
    season integer NOT NULL,
    g integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    pa integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    lob_p numeric,
    era numeric,
    ra_9 numeric,
    so_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric,
    lg_r_pa numeric,
    bsr_bmult numeric,
    bsr numeric,
    bsr_9 numeric,
    fip_constant numeric,
    fip numeric,
    raa numeric,
    bsraa numeric,
    fipraa numeric,
    era_minus numeric,
    fip_minus numeric,
    bsr_minus numeric
);


--
-- Name: name_corrections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.name_corrections (
    uc_fname character varying(20) NOT NULL,
    uc_lname character varying(20) NOT NULL,
    uc_team character varying(5) NOT NULL,
    uc_season integer NOT NULL,
    c_fname character varying(20) NOT NULL,
    c_lname character varying(20) NOT NULL,
    type character(1),
    submitted timestamp without time zone DEFAULT now()
);


--
-- Name: TABLE name_corrections; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.name_corrections IS 'Corrections for player names';


--
-- Name: nicknames; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.nicknames (
    rid integer,
    name character varying(20) NOT NULL,
    nickname character varying(20) NOT NULL
);


--
-- Name: TABLE nicknames; Type: COMMENT; Schema: public; Owner: -
--

COMMENT ON TABLE public.nicknames IS 'Lookup table of common nicknames';


--
-- Name: pitchers_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pitchers_conference (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric,
    ra_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: pitchers_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pitchers_conference_inseason (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric,
    ra_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: pitchers_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pitchers_overall (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    pa integer,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    lob_p numeric,
    era numeric,
    ra_9 numeric,
    so_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: pitchers_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pitchers_overall_inseason (
    no integer,
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    pa integer,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    lob_p numeric,
    era numeric,
    ra_9 numeric,
    so_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: player_id; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.player_id (
    fname character varying(20) NOT NULL,
    lname character varying(20) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    player_id character varying(10)
);


--
-- Name: raw_batters_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_batters_conference (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_batters_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_batters_conference_inseason (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer,
    date date NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_batters_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_batters_overall (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_batters_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_batters_overall_inseason (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer,
    date date NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_game_log_fielding; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_game_log_fielding (
    game_num integer NOT NULL,
    date character varying(10) NOT NULL,
    season integer NOT NULL,
    name character varying(30) NOT NULL,
    opponent text,
    score character varying(10),
    tc integer,
    po integer,
    a integer,
    e integer,
    fpct numeric,
    dp integer,
    sba integer,
    cs integer,
    cspct numeric,
    pb integer,
    ci integer
);


--
-- Name: raw_game_log_fielding_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_game_log_fielding_inseason (
    game_num integer NOT NULL,
    scrape_date date NOT NULL,
    date character varying(10),
    season integer,
    name character varying(30) NOT NULL,
    opponent text,
    score character varying(10),
    tc integer,
    po integer,
    a integer,
    e integer,
    fpct numeric,
    dp integer,
    sba integer,
    cs integer,
    cspct numeric,
    pb integer,
    ci integer
);


--
-- Name: raw_game_log_hitting; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_game_log_hitting (
    game_num integer NOT NULL,
    date character varying(10) NOT NULL,
    season integer NOT NULL,
    name character varying(30) NOT NULL,
    opponent text,
    score character varying(10),
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric,
    pa integer
);


--
-- Name: raw_game_log_hitting_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_game_log_hitting_inseason (
    game_num integer NOT NULL,
    scrape_date date NOT NULL,
    date character varying(10),
    season integer,
    name character varying(30) NOT NULL,
    opponent text,
    score character varying(10),
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric,
    pa integer
);


--
-- Name: raw_game_log_pitching; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_game_log_pitching (
    game_num integer NOT NULL,
    date character varying(10) NOT NULL,
    season integer NOT NULL,
    name character varying(30) NOT NULL,
    opponent text,
    score character varying(10),
    w integer,
    l integer,
    sv integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    era numeric,
    bb integer,
    so integer,
    hr integer
);


--
-- Name: raw_game_log_pitching_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_game_log_pitching_inseason (
    game_num integer NOT NULL,
    scrape_date date NOT NULL,
    date character varying(10),
    season integer,
    name character varying(30) NOT NULL,
    opponent text,
    score character varying(10),
    w integer,
    l integer,
    sv integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    era numeric,
    bb integer,
    so integer,
    hr integer
);


--
-- Name: raw_pitchers_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_pitchers_conference (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character varying(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric
);


--
-- Name: raw_pitchers_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_pitchers_conference_inseason (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer,
    date date NOT NULL,
    yr character varying(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric
);


--
-- Name: raw_pitchers_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_pitchers_overall (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    era numeric,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    avg numeric,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    so_9 numeric
);


--
-- Name: raw_pitchers_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_pitchers_overall_inseason (
    no integer,
    name character varying(35) NOT NULL,
    team character varying(5) NOT NULL,
    season integer,
    date date NOT NULL,
    yr character(2),
    pos character varying(15),
    g integer,
    gs integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    era numeric,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    avg numeric,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    so_9 numeric
);


--
-- Name: raw_team_fielding_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_fielding_conference (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    tc integer,
    po integer,
    a integer,
    e integer,
    fpct numeric,
    dp integer,
    sba integer,
    cs integer,
    cspct numeric,
    pb integer,
    ci integer
);


--
-- Name: raw_team_fielding_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_fielding_conference_inseason (
    name character varying(30) NOT NULL,
    season integer,
    date date NOT NULL,
    g integer,
    tc integer,
    po integer,
    a integer,
    e integer,
    fpct numeric,
    dp integer,
    sba integer,
    cs integer,
    cspct numeric,
    pb integer,
    ci integer
);


--
-- Name: raw_team_fielding_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_fielding_overall (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    tc integer,
    po integer,
    a integer,
    e integer,
    fpct numeric,
    dp integer,
    sba integer,
    cs integer,
    cspct numeric,
    pb integer,
    ci integer
);


--
-- Name: raw_team_fielding_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_fielding_overall_inseason (
    name character varying(30) NOT NULL,
    season integer,
    date date NOT NULL,
    g integer,
    tc integer,
    po integer,
    a integer,
    e integer,
    fpct numeric,
    dp integer,
    sba integer,
    cs integer,
    cspct numeric,
    pb integer,
    ci integer
);


--
-- Name: raw_team_offense_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_offense_conference (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_team_offense_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_offense_conference_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_team_offense_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_offense_overall (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_team_offense_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_offense_overall_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    sb integer,
    cs integer,
    avg numeric,
    obp numeric,
    slg numeric,
    hbp integer,
    sf integer,
    sh integer,
    tb integer,
    xbh integer,
    gdp integer,
    go integer,
    fo integer,
    go_fo numeric
);


--
-- Name: raw_team_pitching_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_pitching_conference (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric
);


--
-- Name: raw_team_pitching_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_pitching_conference_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric
);


--
-- Name: raw_team_pitching_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_pitching_overall (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    era numeric,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    avg numeric,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    so_9 numeric
);


--
-- Name: raw_team_pitching_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.raw_team_pitching_overall_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip character varying(20),
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    era numeric,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    avg numeric,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    so_9 numeric
);


--
-- Name: replacement_level_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.replacement_level_conference (
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    sbr numeric,
    wsb numeric,
    woba numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    off_pa numeric
);


--
-- Name: replacement_level_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.replacement_level_overall (
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    sar numeric,
    sbr numeric,
    wsb numeric,
    woba numeric,
    wraa numeric,
    off numeric,
    wrc numeric,
    wrc_p numeric,
    off_p numeric,
    off_pa numeric
);


--
-- Name: team_ids; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_ids (
    name character varying(30),
    id character varying(5)
);


--
-- Name: team_offense_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_offense_conference (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: team_offense_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_offense_conference_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: team_offense_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_offense_overall (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: team_offense_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_offense_overall_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    pa integer,
    ab integer,
    r integer,
    h integer,
    x2b integer,
    x3b integer,
    hr integer,
    rbi integer,
    bb integer,
    so integer,
    hbp integer,
    tb integer,
    xbh integer,
    sf integer,
    sh integer,
    gdp integer,
    sb integer,
    cs integer,
    go integer,
    fo integer,
    go_fo numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    babip numeric,
    iso numeric,
    avg numeric,
    obp numeric,
    slg numeric,
    ops numeric,
    sar numeric
);


--
-- Name: team_pitching_conference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_pitching_conference (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric,
    ra_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: team_pitching_conference_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_pitching_conference_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    so_9 numeric,
    hr integer,
    era numeric,
    ra_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: team_pitching_overall; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_pitching_overall (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    g integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    era numeric,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    avg numeric,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    so_9 numeric,
    pa integer,
    obp numeric,
    slg numeric,
    ops numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    lob_p numeric,
    ra_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: team_pitching_overall_inseason; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.team_pitching_overall_inseason (
    name character varying(30) NOT NULL,
    season integer NOT NULL,
    date date NOT NULL,
    g integer,
    w integer,
    l integer,
    sv integer,
    cg integer,
    sho integer,
    ip numeric,
    h integer,
    r integer,
    er integer,
    bb integer,
    so integer,
    era numeric,
    x2b integer,
    x3b integer,
    hr integer,
    ab integer,
    avg numeric,
    wp integer,
    hbp integer,
    bk integer,
    sf integer,
    sh integer,
    so_9 numeric,
    pa integer,
    obp numeric,
    slg numeric,
    ops numeric,
    hbp_p numeric,
    bb_p numeric,
    so_p numeric,
    iso numeric,
    babip numeric,
    lob_p numeric,
    ra_9 numeric,
    bb_9 numeric,
    hr_9 numeric,
    whip numeric
);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: batters_conference_inseason batters_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.batters_conference_inseason
    ADD CONSTRAINT batters_conference_inseason_pkey PRIMARY KEY (fname, lname, team, season, date);


--
-- Name: batters_conference batters_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.batters_conference
    ADD CONSTRAINT batters_conference_pkey PRIMARY KEY (fname, lname, team, season);


--
-- Name: batters_overall_inseason batters_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.batters_overall_inseason
    ADD CONSTRAINT batters_overall_inseason_pkey PRIMARY KEY (fname, lname, team, season, date);


--
-- Name: batters_overall batters_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.batters_overall
    ADD CONSTRAINT batters_overall_pkey PRIMARY KEY (fname, lname, team, season);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: duplicate_names duplicate_names_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.duplicate_names
    ADD CONSTRAINT duplicate_names_pkey PRIMARY KEY (fname, lname, team, season);


--
-- Name: game_log_inseason game_log_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_log_inseason
    ADD CONSTRAINT game_log_inseason_pkey PRIMARY KEY (scrape_date, game_num, season, team);


--
-- Name: game_log game_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.game_log
    ADD CONSTRAINT game_log_pkey PRIMARY KEY (game_num, season, team);


--
-- Name: league_offense_conference_inseason league_offense_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.league_offense_conference_inseason
    ADD CONSTRAINT league_offense_conference_inseason_pkey PRIMARY KEY (date);


--
-- Name: league_offense_conference league_offense_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.league_offense_conference
    ADD CONSTRAINT league_offense_conference_pkey PRIMARY KEY (season);


--
-- Name: league_offense_overall_inseason league_offense_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.league_offense_overall_inseason
    ADD CONSTRAINT league_offense_overall_inseason_pkey PRIMARY KEY (date);


--
-- Name: league_offense_overall league_offense_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.league_offense_overall
    ADD CONSTRAINT league_offense_overall_pkey PRIMARY KEY (season);


--
-- Name: league_pitching_conference league_pitching_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.league_pitching_conference
    ADD CONSTRAINT league_pitching_conference_pkey PRIMARY KEY (season);


--
-- Name: league_pitching_overall league_pitching_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.league_pitching_overall
    ADD CONSTRAINT league_pitching_overall_pkey PRIMARY KEY (season);


--
-- Name: name_corrections name_corrections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.name_corrections
    ADD CONSTRAINT name_corrections_pkey PRIMARY KEY (uc_fname, uc_lname, uc_team, uc_season);


--
-- Name: nicknames nicknames_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.nicknames
    ADD CONSTRAINT nicknames_pkey PRIMARY KEY (name, nickname);


--
-- Name: pitchers_conference_inseason pitchers_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pitchers_conference_inseason
    ADD CONSTRAINT pitchers_conference_inseason_pkey PRIMARY KEY (fname, lname, team, season, date);


--
-- Name: pitchers_conference pitchers_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pitchers_conference
    ADD CONSTRAINT pitchers_conference_pkey PRIMARY KEY (fname, lname, team, season);


--
-- Name: pitchers_overall_inseason pitchers_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pitchers_overall_inseason
    ADD CONSTRAINT pitchers_overall_inseason_pkey PRIMARY KEY (fname, lname, team, season, date);


--
-- Name: pitchers_overall pitchers_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pitchers_overall
    ADD CONSTRAINT pitchers_overall_pkey PRIMARY KEY (fname, lname, team, season);


--
-- Name: player_id player_id_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.player_id
    ADD CONSTRAINT player_id_pkey PRIMARY KEY (fname, lname, team, season);


--
-- Name: raw_batters_conference_inseason raw_batters_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_batters_conference_inseason
    ADD CONSTRAINT raw_batters_conference_inseason_pkey PRIMARY KEY (name, team, date);


--
-- Name: raw_batters_conference raw_batters_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_batters_conference
    ADD CONSTRAINT raw_batters_conference_pkey PRIMARY KEY (name, team, season);


--
-- Name: raw_batters_overall_inseason raw_batters_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_batters_overall_inseason
    ADD CONSTRAINT raw_batters_overall_inseason_pkey PRIMARY KEY (name, team, date);


--
-- Name: raw_batters_overall raw_batters_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_batters_overall
    ADD CONSTRAINT raw_batters_overall_pkey PRIMARY KEY (name, team, season);


--
-- Name: raw_game_log_fielding_inseason raw_game_log_fielding_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_game_log_fielding_inseason
    ADD CONSTRAINT raw_game_log_fielding_inseason_pkey PRIMARY KEY (game_num, scrape_date, name);


--
-- Name: raw_game_log_fielding raw_game_log_fielding_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_game_log_fielding
    ADD CONSTRAINT raw_game_log_fielding_pkey PRIMARY KEY (game_num, date, season, name);


--
-- Name: raw_game_log_hitting_inseason raw_game_log_hitting_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_game_log_hitting_inseason
    ADD CONSTRAINT raw_game_log_hitting_inseason_pkey PRIMARY KEY (game_num, scrape_date, name);


--
-- Name: raw_game_log_hitting raw_game_log_hitting_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_game_log_hitting
    ADD CONSTRAINT raw_game_log_hitting_pkey PRIMARY KEY (game_num, date, season, name);


--
-- Name: raw_game_log_pitching_inseason raw_game_log_pitching_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_game_log_pitching_inseason
    ADD CONSTRAINT raw_game_log_pitching_inseason_pkey PRIMARY KEY (game_num, scrape_date, name);


--
-- Name: raw_game_log_pitching raw_game_log_pitching_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_game_log_pitching
    ADD CONSTRAINT raw_game_log_pitching_pkey PRIMARY KEY (game_num, date, season, name);


--
-- Name: raw_pitchers_conference_inseason raw_pitchers_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_pitchers_conference_inseason
    ADD CONSTRAINT raw_pitchers_conference_inseason_pkey PRIMARY KEY (name, team, date);


--
-- Name: raw_pitchers_conference raw_pitchers_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_pitchers_conference
    ADD CONSTRAINT raw_pitchers_conference_pkey PRIMARY KEY (name, team, season);


--
-- Name: raw_pitchers_overall_inseason raw_pitchers_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_pitchers_overall_inseason
    ADD CONSTRAINT raw_pitchers_overall_inseason_pkey PRIMARY KEY (name, team, date);


--
-- Name: raw_pitchers_overall raw_pitchers_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_pitchers_overall
    ADD CONSTRAINT raw_pitchers_overall_pkey PRIMARY KEY (name, team, season);


--
-- Name: raw_team_fielding_conference_inseason raw_team_fielding_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_fielding_conference_inseason
    ADD CONSTRAINT raw_team_fielding_conference_inseason_pkey PRIMARY KEY (name, date);


--
-- Name: raw_team_fielding_conference raw_team_fielding_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_fielding_conference
    ADD CONSTRAINT raw_team_fielding_conference_pkey PRIMARY KEY (name, season);


--
-- Name: raw_team_fielding_overall_inseason raw_team_fielding_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_fielding_overall_inseason
    ADD CONSTRAINT raw_team_fielding_overall_inseason_pkey PRIMARY KEY (name, date);


--
-- Name: raw_team_fielding_overall raw_team_fielding_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_fielding_overall
    ADD CONSTRAINT raw_team_fielding_overall_pkey PRIMARY KEY (name, season);


--
-- Name: raw_team_offense_conference_inseason raw_team_offense_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_offense_conference_inseason
    ADD CONSTRAINT raw_team_offense_conference_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: raw_team_offense_conference raw_team_offense_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_offense_conference
    ADD CONSTRAINT raw_team_offense_conference_pkey PRIMARY KEY (name, season);


--
-- Name: raw_team_offense_overall_inseason raw_team_offense_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_offense_overall_inseason
    ADD CONSTRAINT raw_team_offense_overall_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: raw_team_offense_overall raw_team_offense_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_offense_overall
    ADD CONSTRAINT raw_team_offense_overall_pkey PRIMARY KEY (name, season);


--
-- Name: raw_team_pitching_conference_inseason raw_team_pitching_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_pitching_conference_inseason
    ADD CONSTRAINT raw_team_pitching_conference_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: raw_team_pitching_conference raw_team_pitching_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_pitching_conference
    ADD CONSTRAINT raw_team_pitching_conference_pkey PRIMARY KEY (name, season);


--
-- Name: raw_team_pitching_overall_inseason raw_team_pitching_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_pitching_overall_inseason
    ADD CONSTRAINT raw_team_pitching_overall_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: raw_team_pitching_overall raw_team_pitching_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.raw_team_pitching_overall
    ADD CONSTRAINT raw_team_pitching_overall_pkey PRIMARY KEY (name, season);


--
-- Name: replacement_level_conference replacement_level_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.replacement_level_conference
    ADD CONSTRAINT replacement_level_conference_pkey PRIMARY KEY (season);


--
-- Name: replacement_level_overall replacement_level_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.replacement_level_overall
    ADD CONSTRAINT replacement_level_overall_pkey PRIMARY KEY (season);


--
-- Name: team_offense_conference_inseason team_offense_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_offense_conference_inseason
    ADD CONSTRAINT team_offense_conference_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: team_offense_conference team_offense_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_offense_conference
    ADD CONSTRAINT team_offense_conference_pkey PRIMARY KEY (name, season);


--
-- Name: team_offense_overall_inseason team_offense_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_offense_overall_inseason
    ADD CONSTRAINT team_offense_overall_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: team_offense_overall team_offense_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_offense_overall
    ADD CONSTRAINT team_offense_overall_pkey PRIMARY KEY (name, season);


--
-- Name: team_pitching_conference_inseason team_pitching_conference_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_pitching_conference_inseason
    ADD CONSTRAINT team_pitching_conference_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: team_pitching_conference team_pitching_conference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_pitching_conference
    ADD CONSTRAINT team_pitching_conference_pkey PRIMARY KEY (name, season);


--
-- Name: team_pitching_overall_inseason team_pitching_overall_inseason_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_pitching_overall_inseason
    ADD CONSTRAINT team_pitching_overall_inseason_pkey PRIMARY KEY (name, season, date);


--
-- Name: team_pitching_overall team_pitching_overall_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.team_pitching_overall
    ADD CONSTRAINT team_pitching_overall_pkey PRIMARY KEY (name, season);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: batters_conference fk_batters_conference_fname_player_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.batters_conference
    ADD CONSTRAINT fk_batters_conference_fname_player_id FOREIGN KEY (fname, lname, team, season) REFERENCES public.player_id(fname, lname, team, season) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: batters_overall fk_batters_overall_fname_player_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.batters_overall
    ADD CONSTRAINT fk_batters_overall_fname_player_id FOREIGN KEY (fname, lname, team, season) REFERENCES public.player_id(fname, lname, team, season) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: pitchers_conference fk_pitchers_conference_fname_player_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pitchers_conference
    ADD CONSTRAINT fk_pitchers_conference_fname_player_id FOREIGN KEY (fname, lname, team, season) REFERENCES public.player_id(fname, lname, team, season) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: pitchers_overall fk_pitchers_overall_fname_player_id; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pitchers_overall
    ADD CONSTRAINT fk_pitchers_overall_fname_player_id FOREIGN KEY (fname, lname, team, season) REFERENCES public.player_id(fname, lname, team, season) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

