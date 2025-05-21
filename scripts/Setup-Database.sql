-- Create the database if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'EquityShield')
BEGIN
    CREATE DATABASE EquityShield;
END
GO

USE EquityShield;
GO

-- Create CorporateData table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CorporateData]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[CorporateData](
        [Id] [int] IDENTITY(1,1) PRIMARY KEY,
        [CorporateId] [varchar](50) NOT NULL,
        [Name] [varchar](255) NOT NULL,
        [Type] [varchar](100) NOT NULL,
        [CreatedAt] [datetime] DEFAULT GETDATE(),
        [UpdatedAt] [datetime] DEFAULT GETDATE()
    )

    -- Insert sample data
    INSERT INTO [dbo].[CorporateData] (CorporateId, Name, Type)
    VALUES ('ESA-001', 'Equity Shield Advocates', 'Financial Services');
END
GO

-- Create CorporateStructure table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[CorporateStructure]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[CorporateStructure](
        [Id] [int] IDENTITY(1,1) PRIMARY KEY,
        [DepartmentId] [varchar](50) NOT NULL,
        [DepartmentName] [varchar](255) NOT NULL,
        [ParentDepartmentId] [varchar](50) NULL,
        [CreatedAt] [datetime] DEFAULT GETDATE(),
        [UpdatedAt] [datetime] DEFAULT GETDATE()
    )

    -- Insert sample data
    INSERT INTO [dbo].[CorporateStructure] (DepartmentId, DepartmentName, ParentDepartmentId)
    VALUES 
        ('DEP-001', 'Finance', NULL),
        ('DEP-002', 'Legal', NULL),
        ('DEP-003', 'Operations', NULL);
END
GO

-- Create RealAssets table if it doesn't exist
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[RealAssets]') AND type in (N'U'))
BEGIN
    CREATE TABLE [dbo].[RealAssets](
        [Id] [int] IDENTITY(1,1) PRIMARY KEY,
        [AssetId] [varchar](50) NOT NULL,
        [AssetName] [varchar](255) NOT NULL,
        [Category] [varchar](100) NOT NULL,
        [Value] [decimal](18,2) NOT NULL,
        [CreatedAt] [datetime] DEFAULT GETDATE(),
        [UpdatedAt] [datetime] DEFAULT GETDATE()
    )

    -- Insert sample data
    INSERT INTO [dbo].[RealAssets] (AssetId, AssetName, Category, Value)
    VALUES 
        ('AST-001', 'Office Building', 'Property', 500000.00),
        ('AST-002', 'IT Equipment', 'Equipment', 100000.00),
        ('AST-003', 'Investment Portfolio', 'Investments', 400000.00);
END
GO

-- Grant permissions to the current user
DECLARE @CurrentUser nvarchar(100) = SYSTEM_USER;
DECLARE @SQL nvarchar(MAX);

SET @SQL = 'USE [EquityShield]; 
           GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[CorporateData] TO [' + @CurrentUser + '];
           GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[CorporateStructure] TO [' + @CurrentUser + '];
           GRANT SELECT, INSERT, UPDATE, DELETE ON [dbo].[RealAssets] TO [' + @CurrentUser + '];';

EXEC sp_executesql @SQL;
GO
