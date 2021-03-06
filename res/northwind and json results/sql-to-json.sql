SELECT '[' +  STUFF((SELECT
		',{'
		+	'"ProductID":' + CAST([ProductID] AS VARCHAR(30))		+ ','
		+	'"ProductName":"' + CAST([ProductName] AS VARCHAR(30))	+ '",'
		+	'"SupplierID":' + CAST([SupplierID] AS VARCHAR(30))	+ ','
		+	'"CategoryID":' + CAST([CategoryID] AS VARCHAR(30))	+ ','
		+	'"QuantityPerUnit":"' + CAST([QuantityPerUnit] AS VARCHAR(30))	+ '",'
		+	'"UnitPrice":' + CAST([UnitPrice] AS VARCHAR(30))
		+ '}'
FROM Products
FOR XML PATH(''),TYPE).value('.','NVARCHAR(MAX)'),1,1,'') + ']'

--#-------------------------------------------------- BEGIN [generic store procedure] - (25-10-2017 - 15:01:51) {{
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

alter PROCEDURE [dbo].[SerializeJSON] (@ParameterSQL AS VARCHAR(MAX))
AS
BEGIN
    DECLARE @SQL NVARCHAR(MAX)
    DECLARE @XMLString VARCHAR(MAX)
    DECLARE @XML XML
    DECLARE @Paramlist NVARCHAR(1000)

    SET @Paramlist = N'@XML XML OUTPUT'
    SET @SQL = 'WITH PrepareTable (XMLString)'
    SET @SQL = @SQL + 'AS('
    SET @SQL = @SQL + @ParameterSQL + ' FOR XML RAW,TYPE,ELEMENTS'
    SET @SQL = @SQL + ')'
    SET @SQL = @SQL + 'SELECT @XML=[XMLString]FROM[PrepareTable]'

    EXEC sp_executesql @SQL
        , @Paramlist
        , @XML = @XML OUTPUT

    SET @XMLString = CAST(@XML AS VARCHAR(MAX))

    DECLARE @JSON VARCHAR(MAX)
    DECLARE @Row VARCHAR(MAX)
    DECLARE @RowStart INT
    DECLARE @RowEnd INT
    DECLARE @FieldStart INT
    DECLARE @FieldEnd INT
    DECLARE @KEY VARCHAR(MAX)
    DECLARE @Value VARCHAR(MAX)
    DECLARE @StartRoot VARCHAR(100);

    SET @StartRoot = '<row>'

    DECLARE @EndRoot VARCHAR(100);

    SET @EndRoot = '</row>'

    DECLARE @StartField VARCHAR(100);

    SET @StartField = '<'

    DECLARE @EndField VARCHAR(100);

    SET @EndField = '>'
    SET @RowStart = CharIndex(@StartRoot, @XMLString, 0)
    SET @JSON = ''

    WHILE @RowStart > 0
    BEGIN
        SET @RowStart = @RowStart + Len(@StartRoot)
        SET @RowEnd = CharIndex(@EndRoot, @XMLString, @RowStart)
        SET @Row = SubString(@XMLString, @RowStart, @RowEnd - @RowStart)
        SET @JSON = @JSON + '{'
        -- for each row
        SET @FieldStart = CharIndex(@StartField, @Row, 0)

        WHILE @FieldStart > 0
        BEGIN
            -- parse node key
            SET @FieldStart = @FieldStart + Len(@StartField)
            SET @FieldEnd = CharIndex(@EndField, @Row, @FieldStart)
            SET @KEY = SubString(@Row, @FieldStart, @FieldEnd - @FieldStart)
            SET @JSON = @JSON + '"' + @KEY + '":'
            -- parse node value
            SET @FieldStart = @FieldEnd + 1
            SET @FieldEnd = CharIndex('</', @Row, @FieldStart)
            SET @Value = SubString(@Row, @FieldStart, @FieldEnd - @FieldStart)
            SET @JSON = @JSON + '"' + @Value + '",'
            SET @FieldStart = @FieldStart + Len(@StartField)
            SET @FieldEnd = CharIndex(@EndField, @Row, @FieldStart)
            SET @FieldStart = CharIndex(@StartField, @Row, @FieldEnd)
        END

        IF LEN(@JSON) > 0
            SET @JSON = SubString(@JSON, 0, LEN(@JSON))
        SET @JSON = @JSON + '},'
        --/ for each row
        SET @RowStart = CharIndex(@StartRoot, @XMLString, @RowEnd)
    END

    IF LEN(@JSON) > 0
        SET @JSON = SubString(@JSON, 0, LEN(@JSON))
    SET @JSON = '[' + @JSON + ']'

    SELECT @JSON
END

EXEC [dbo].[SerializeJSON] 'SELECT * FROM Products'
--#-------------------------------------------------- END   [generic store procedure] - (25-10-2017 - 15:01:51) }}
--https://nyquist212.wordpress.com/2014/02/11/tsql-to-json-2/comment-page-1/
