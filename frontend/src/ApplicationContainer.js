import ApplicationList from "./ApplicationList";
import useFetch from "./useFetch";


const ApplicationContainer = () => {
    const { error, isPending, data: apps } = useFetch('http://127.0.0.1/api/apps')

  return (
    <div className="container">
    { error && <div>{ error }</div> }
    { isPending && <div>Loading...</div> }
    {apps &&<ApplicationList apps={apps} />}
    </div>
  );
}
 
export default ApplicationContainer;
