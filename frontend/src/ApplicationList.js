const ApplicationList = ({ apps }) => {
    return (
      <div className="app-list">
        {apps.map(app => (
          <div className="app-preview" key={app.id} >
            <h2>{ app.name }</h2>
            <p>Version { app.version }</p>
          </div>
        ))}
      </div>
    );
  }
   
  export default ApplicationList;