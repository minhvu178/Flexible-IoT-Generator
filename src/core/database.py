# src/core/database.py
import pymongo
import json
import os

class Database:
    """Database connectivity manager."""
    
    def __init__(self, config):
        """
        Initialize database connection based on configuration.
        
        Args:
            config: Database configuration dict (type, connection params)
        """
        self.config = config
        self.db_type = config.get('type', 'none')
        self.connection = None
        self.collection = None
        
        if self.db_type == 'mongodb':
            self._connect_mongodb()
        elif self.db_type == 'file':
            self._setup_file_storage()
    
    def _connect_mongodb(self):
        """Connect to MongoDB database."""
        conn_config = self.config['connection']
        host = conn_config.get('host', 'localhost')
        port = conn_config.get('port', 27017)
        username = conn_config.get('username', '')
        password = conn_config.get('password', '')
        
        # Build connection string
        if username and password:
            uri = f"mongodb://{username}:{password}@{host}:{port}/"
        else:
            uri = f"mongodb://{host}:{port}/"
            
        try:
            # Connect to MongoDB
            self.connection = pymongo.MongoClient(uri)
            
            # Get database and collection
            db_name = conn_config.get('database', 'iot_data')
            coll_name = conn_config.get('collection', 'sensor_data')
            
            self.db = self.connection[db_name]
            self.collection = self.db[coll_name]
            
            # Check if collection should be a time series collection
            if conn_config.get('time_series', True) and coll_name not in self.db.list_collection_names():
                # Create time series collection
                self.db.create_collection(
                    coll_name,
                    timeseries={
                        'timeField': 'timestamp',
                        'metaField': 'metadata',
                        'granularity': conn_config.get('granularity', 'seconds')
                    }
                )
                self.collection = self.db[coll_name]
                
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
    
    def _setup_file_storage(self):
        """Set up file-based storage."""
        path = self.config['connection'].get('path', 'data/files')
        
        # Create directory if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
            
        self.file_path = path
    
    def insert_one(self, document):
        """
        Insert a single document.
        
        Args:
            document: Document to insert
            
        Returns:
            Result of insertion
        """
        if self.db_type == 'mongodb':
            return self.collection.insert_one(document)
        elif self.db_type == 'file':
            # Generate filename based on metadata
            if 'metadata' in document:
                filename = f"{document['metadata'].get('factoryId', 'unknown')}_"
                filename += f"{document['metadata'].get('deviceId', 'unknown')}_"
                filename += f"{document['metadata'].get('sensorId', 'unknown')}.json"
            else:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = f"data_{timestamp}.json"
            
            filepath = os.path.join(self.file_path, filename)
            
            # Append to file
            with open(filepath, 'a') as f:
                f.write(json.dumps(document) + '\n')
                
            return True
    
    def insert_many(self, documents):
        """
        Insert multiple documents.
        
        Args:
            documents: List of documents to insert
            
        Returns:
            Result of insertion
        """
        if self.db_type == 'mongodb':
            return self.collection.insert_many(documents)
        elif self.db_type == 'file':
            # Group documents by factory/device/sensor
            grouped = {}
            
            for doc in documents:
                if 'metadata' in doc:
                    key = (
                        doc['metadata'].get('factoryId', 'unknown'),
                        doc['metadata'].get('deviceId', 'unknown'),
                        doc['metadata'].get('sensorId', 'unknown')
                    )
                else:
                    key = ('unknown', 'unknown', 'unknown')
                
                if key not in grouped:
                    grouped[key] = []
                    
                grouped[key].append(doc)
            
            # Write each group to its own file
            for (factory_id, device_id, sensor_id), docs in grouped.items():
                filename = f"{factory_id}_{device_id}_{sensor_id}.json"
                filepath = os.path.join(self.file_path, filename)
                
                with open(filepath, 'a') as f:
                    for doc in docs:
                        f.write(json.dumps(doc) + '\n')
            
            return True