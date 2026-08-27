/* BUILD TRACE: BT-001
 * PURPOSE: Application Header Shell
 * RESEARCH CONNECTION: Application navigation
 */
import { NavLink, useLocation, useNavigate } from 'react-router-dom';

const INDUSTRIES = [
  ['Aviation & Aerospace', 'Aviation & Aerospace'],
  ['B2B & Commerce', 'B2B & Commerce'],
  ['Consumer & Retail', 'Consumer & Retail'],
  ['Financial Services', 'Financial Services'],
  ['Healthcare / Hospital Operations', 'Healthcare'],
  ['IT & Business Services', 'IT & Business Services'],
  ['Logistics & Supply Chain', 'Logistics & Supply Chain'],
  ['Manufacturing & Engineering', 'Manufacturing & Engineering'],
] as const;

export function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const selectedIndustry = location.pathname === '/walkthrough'
    ? new URLSearchParams(location.search).get('industry') ?? ''
    : '';

  return (
    <header className="header">
      <div className="header-identity">
        <div className="header-subject">
          <NavLink to="/">
            <img src="/brand-assets/ail-header.png" alt="A Realtime Tech" className="brand-logo" />
          </NavLink>
        </div>
      </div>

      <div className="header-controls" style={{ display: 'flex', gap: '0.5rem', justifyContent: 'center', flex: 1 }}>
        <NavLink
          to="/walkthrough"
          className={({ isActive }) => 'btn-header ' + (isActive ? 'active' : '')}
        >
          WALKTHROUGH
        </NavLink>
        <NavLink
          to="/workflow"
          className={({ isActive }) => 'btn-header ' + (isActive ? 'active' : '')}
        >
          WORKFLOW
        </NavLink>
      </div>

      <div className="header-right" style={{ display: 'flex', justifyContent: 'flex-end', flex: 1, paddingRight: '1rem', alignItems: 'center' }}>
        <select
          className="btn-header"
          value={selectedIndustry}
          aria-label="Choose an industry"
          onChange={event => {
            const industry = event.target.value;
            if (industry) navigate('/walkthrough?industry=' + encodeURIComponent(industry));
          }}
          style={{ appearance: 'auto', padding: '0.4rem 0.8rem', backgroundColor: '#fff', color: '#333' }}
        >
          <option value="" disabled>Industries</option>
          {INDUSTRIES.map(([value, label]) => <option value={value} key={value}>{label}</option>)}
        </select>
      </div>
    </header>
  );
}
