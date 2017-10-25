
CREATE PROCEDURE [dbo].[GetCustomers_Pager]
      @PageIndex INT = 1
      ,@PageSize INT = 10
      ,@RecordCount INT OUTPUT
AS
BEGIN
      SET NOCOUNT ON;
      SELECT ROW_NUMBER() OVER
      (
            ORDER BY [CustomerID] ASC
      )AS RowNumber
      ,[CustomerID]
      ,[CompanyName]
      ,[ContactName]
      ,[City]
      INTO #Results
      FROM [Customers]
     
      SELECT @RecordCount = COUNT(*)
      FROM #Results
           
      SELECT * FROM #Results
      WHERE RowNumber BETWEEN(@PageIndex -1) * @PageSize + 1 AND(((@PageIndex -1) * @PageSize + 1) + @PageSize) - 1
     
      DROP TABLE #Results
END
