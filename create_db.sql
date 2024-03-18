CREATE DATABASE DE_GLOBANT;
USE DE_GLOBANT;

CREATE SCHEMA ing;

CREATE TABLE [ing].[departments](
	[ID] [bigint] NULL,
	[Department] [varchar](max) NULL
) ;
CREATE TABLE [ing].[hired_employees](
	[ID] [bigint] NULL,
	[Name] [varchar](max) NULL,
	[Datetime] [varchar](max) NULL,
	[Department_id] [float] NULL,
	[Job_id] [float] NULL
) ;
CREATE TABLE [ing].[jobs](
	[ID] [bigint] NULL,
	[Job] [varchar](max) NULL
);

CREATE SCHEMA dim;

CREATE TABLE [dim].[departments](
	[ID] [bigint] NULL,
	[Department] [varchar](max) NULL
) ;
CREATE TABLE [dim].[hired_employees](
	[ID] [bigint] NULL,
	[Name] [varchar](max) NULL,
	[Datetime] [varchar](max) NULL,
	[Department_id] [float] NULL,
	[Job_id] [float] NULL
) ;
CREATE TABLE [dim].[jobs](
	[ID] [bigint] NULL,
	[Job] [varchar](max) NULL
);

CREATE SCHEMA rep;

CREATE TABLE [rep].[department_hiring_report](
	[id] [bigint] NULL,
	[department] [varchar](max) NULL,
	[hired] [bigint] NULL
) ;
CREATE TABLE [rep].[hired_employees_summary](
	[Department] [varchar](max) NULL,
	[Job] [varchar](max) NULL,
	[Q1] [bigint] NULL,
	[Q2] [bigint] NULL,
	[Q3] [bigint] NULL,
	[Q4] [bigint] NULL
);