import { useEffect, useState } from "react";
import { getUser } from "../utils/auth";
import {
  getProgressReport,
  getCertificateEligibility,
  downloadCertificate,
  downloadProgressReport,
} from "../services/api";

export default function Reports() {
  const user = getUser();
  const [report, setReport] = useState(null);
  const [eligibility, setEligibility] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        setReport(await getProgressReport(user.id));
        setEligibility(await getCertificateEligibility(user.id));
      } catch (e) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    }
    if (user?.id) load();
  }, []);

  async function saveBlob(blob, name){
    const url = URL.createObjectURL(blob);
    const a=document.createElement("a");
    a.href=url;
    a.download=name;
    a.click();
    URL.revokeObjectURL(url);
  }

  if(loading) return <h2>Loading...</h2>;
  if(error) return <h2>{error}</h2>;

  return (
    <div style={{padding:30}}>
      <h1>Progress Report</h1>

      <p><b>Overall Accuracy:</b> {report.average_accuracy}%</p>
      <p><b>Lessons Completed:</b> {report.lessons_completed}</p>
      <p><b>Total Attempts:</b> {report.total_attempts}</p>
      <p><b>Practice Time:</b> {(report.total_practice_time/3600).toFixed(2)} hours</p>

      <h2>Attempted Letters</h2>
      <ul>
      {report.attempted_letters.map(l=><li key={l}>{l}</li>)}
      </ul>

      <h2>Weak Letters</h2>
      {report.weak_letters.length===0 ? <p>None 🎉</p> :
      <ul>{report.weak_letters.map(l=><li key={l}>{l}</li>)}</ul>}

      <h2>Certificate</h2>
      {eligibility?.eligible ?
      <>
      <p>Eligible ✅</p>
      <button onClick={async()=>saveBlob(await downloadCertificate(user.id,user.name||user.full_name||"Learner"),"Certificate.pdf")}>Download Certificate</button>
      </>
      :
      <>
      <p>Not Eligible ❌</p>
      <p>Missing: {eligibility?.missing_letters?.join(", ")}</p>
      </>}

      <br/><br/>
      <button onClick={async()=>saveBlob(await downloadProgressReport(user.id,user.name||user.full_name||"Learner"),"Progress_Report.pdf")}>Download Progress Report</button>
    </div>
  );
}
