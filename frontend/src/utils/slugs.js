export const makeTeamSlug = (name) => {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
};

export const makeMatchSlug = (homeTeam, awayTeam) => {
  return `${makeTeamSlug(homeTeam)}-vs-${makeTeamSlug(awayTeam)}`;
};