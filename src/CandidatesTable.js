import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ItemsTable = () => {
    const [items, setItems] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await axios.get(''); // Replace with your API Gateway URL
                setItems(response.data);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
            <h1>Candidates</h1>
            {error && <p>Error: {error}</p>}
            <table>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Requirements</th>
                    </tr>
                </thead>
                <tbody>
                    {items.map((item, index) => (
                        <tr key={index}>
                            <td>{item.name}</td>
                            <td>{item.summary}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ItemsTable;