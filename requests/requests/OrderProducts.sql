SELECT idOrderProducts,
       orderproducts.idProduct,
       Name,
       Quantity,
       Sum
FROM orderproducts
JOIN product ON product.idProduct=orderproducts.idProduct
WHERE idOrder = $idOrder